from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import Payments,PaymentSerializer

# Create your views here.
class PaymentViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    # def get_queryset(self):
    #     return Payments.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)