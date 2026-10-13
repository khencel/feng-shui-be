from rest_framework import serializers
from .models import Payments

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"
        
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]