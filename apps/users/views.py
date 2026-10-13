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
            },
        })