from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import Payments,PaymentSerializer

# Create your views here.
class PaymentViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Payments.objects.all()
        user_id = self.request.query_params.get("user_id")

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset