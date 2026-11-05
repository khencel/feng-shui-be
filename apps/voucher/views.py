from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import Voucher, VoucherSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class VoucherViewSet(ModelViewSet):
    serializer_class = VoucherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Voucher.objects.all()
        user_id = self.request.query_params.get("user_id")

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset
    
    
class CheckVoucherIfValid(APIView):
    def post(self, request):
        code = request.data.get('code')
        user_id = request.data.get('user')


        if not code or not user_id:
            return Response(
                {
                    "valid": False,
                    "message": "Voucher code and user are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

       
        voucher = Voucher.objects.filter(
            code=code,
            user_id=user_id
        ).first()
        

        if voucher is None:
            return Response(
                {
                    "valid": False,
                    "message": "Invalid voucher code."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        voucher.is_used = True
        voucher.save()
        serializer = VoucherSerializer(voucher)
        
        return Response(
            {
                "valid": True,
                "message": "Voucher is valid.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
        