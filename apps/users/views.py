from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from google.oauth2 import id_token  # type: ignore[reportMissingImports]
from google.auth.transport import requests  # type: ignore[reportMissingImports]
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django.db import transaction
from rest_framework.permissions import AllowAny

from rest_framework.generics import RetrieveUpdateAPIView
from apps.users.authentication import getCurrentVoucher
import requests as http_requests

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [SearchFilter]
    search_fields = [
        "first_name",
        "last_name",
        "email",
    ]
    
    @action(
        detail=False,
        methods=["get"],
        url_path="all",
        pagination_class=None
    )
    def all_users(self, request):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)

        return Response(serializer.data)
    
    
class TestApi(APIView):
    def get(self, request):
        return Response("Test")
    

class GoogleLoginView(APIView):

    def post(self, request):
        google_token = request.data.get("id_token")
        

        if not google_token:
            return Response(
                {"detail": "Google ID token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Verify token with Google
            google_user = id_token.verify_oauth2_token(
                google_token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
                clock_skew_in_seconds=10,
            )
            print("GOOGLE USER:", google_user)
            sub = google_user.get("sub")

        except ValueError as e:
            print("GOOGLE TOKEN ERROR:", str(e))
            return Response(
                {"detail": "Invalid Google ID token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        email = google_user.get("email")
        first_name = google_user.get("given_name", "")
        last_name = google_user.get("family_name", "")

        if not email:
            return Response(
                {"detail": "Google account does not have an email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "is_active": True,
                "google_id": sub
            },
        )

        # Update name if existing user
        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.google_id = sub
            user.save(
                update_fields=[
                    "first_name",
                    "last_name",
                    "google_id",
                ]
            )

        # Generate Django JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_of_birth":user.date_of_birth,
                "gender":user.gender,
                "voucher":getCurrentVoucher(user.id)
            },
        })
        
        
class FacebookLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        access_token = request.data.get("access_token")

        if not access_token:
            return Response(
                {"detail": "Facebook access token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        app_id = settings.FACEBOOK_APP_ID
        app_secret = settings.FACEBOOK_APP_SECRET
        api_version = settings.FACEBOOK_API_VERSION

        if not all([app_id, app_secret, api_version]):
            return Response(
                {"detail": "Facebook login is not configured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        base_url = (
            f"https://graph.facebook.com/{api_version}"
        )

        try:
            # 1. Validate token and confirm it belongs to your app
            debug_response = http_requests.get(
                f"{base_url}/debug_token",
                params={
                    "input_token": access_token,
                    "access_token": f"{app_id}|{app_secret}",
                },
                timeout=10,
            )
            debug_response.raise_for_status()

            token_data = debug_response.json().get("data", {})

            if (
                not token_data.get("is_valid")
                or str(token_data.get("app_id")) != str(app_id)
            ):
                return Response(
                    {"detail": "Invalid Facebook access token."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # 2. Get Facebook profile
            profile_response = http_requests.get(
                f"{base_url}/me",
                params={
                    "fields": "id,first_name,last_name,email",
                    "access_token": access_token,
                },
                timeout=10,
            )
            profile_response.raise_for_status()

            facebook_user = profile_response.json()

        except http_requests.RequestException:
            return Response(
                {"detail": "Unable to verify Facebook account."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        facebook_id = facebook_user.get("id")

        # Make sure the returned identity matches the validated token
        if (
            not facebook_id
            or str(token_data.get("user_id")) != str(facebook_id)
        ):
            return Response(
                {"detail": "Facebook identity verification failed."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        email = (facebook_user.get("email") or "").strip().lower()

        if not email:
            return Response(
                {
                    "detail": (
                        "No email was provided by Facebook. "
                        "Please use another login method or complete "
                        "email verification."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        first_name = facebook_user.get("first_name", "")
        last_name = facebook_user.get("last_name", "")

        # 3. Find existing account by Facebook ID
        user = User.objects.filter(
            facebook_id=facebook_id
        ).first()

        if user:
            if not user.is_active:
                return Response(
                    {"detail": "This account is inactive."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        else:
            # Do not automatically link an existing account by email.
            existing_user = User.objects.filter(
                email__iexact=email
            ).first()

            if existing_user:
                return Response(
                    {
                        "detail": (
                            "An account with this email already exists. "
                            "Please sign in using your existing method "
                            "or securely link your Facebook account."
                        )
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            # 4. Create a new Django account
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "facebook_id": facebook_id,
                    "is_active": True,
                },
            )

            if not created:
                return Response(
                    {"detail": "Unable to create Facebook account."},
                    status=status.HTTP_409_CONFLICT,
                )

        # 5. Generate Django JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_of_birth": user.date_of_birth,
                "gender": user.gender,
            },
        })
        
class Registration(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data.copy()

        # Validate password confirmation
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if not password:
            return Response({
                "success": False,
                "message": "Password is required.",
                "errors": {
                    "password": ["This field is required."]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({
                "success": False,
                "message": "Passwords do not match.",
                "errors": {
                    "confirm_password": ["Passwords do not match."]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check existing email
        email = data.get("email", "").strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            return Response({
                "success": False,
                "message": "An account with this email already exists.",
                "errors": {
                    "email": ["This email is already registered."]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Remove confirm_password before serialization
        data["email"] = email
        data.pop("confirm_password", None)

        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()

                return Response({
                    "success": True,
                    "message": "Your account has been registered successfully.",
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "gender": user.gender,
                        "date_of_birth": user.date_of_birth,
                    }
                }, status=status.HTTP_201_CREATED)

            except Exception:
                return Response({
                    "success": False,
                    "message": "Unable to complete registration. Please try again."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "success": False,
            "message": "Please check your registration details.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateProfile(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user