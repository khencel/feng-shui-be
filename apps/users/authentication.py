from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.voucher.serializers import Voucher, VoucherSerializer
from django.utils import timezone

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    
    def validate(self, attrs):
        data = super().validate(attrs)
        

        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "gender": self.user.gender,
            "date_of_birth":self.user.date_of_birth,
            "is_admin": self.user.is_admin,
            "voucher": getCurrentVoucher(self.user.id)
        }

        return data
    
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    
def getCurrentVoucher(id):
    today = timezone.localdate()
    
    voucher = Voucher.objects.filter(
        user_id=id,
        is_used=True,
        expire_date__gte=today
    ).first()
    
    if voucher is None:
        return None
    
    res = VoucherSerializer(voucher, many=False)
    return res.data
    
    