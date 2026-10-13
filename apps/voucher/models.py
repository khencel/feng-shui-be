from django.db import models
from apps.users.models import User

# Create your models here.
class Voucher(models. Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="voucher")
    expire_date = models.DateField(null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "vouchers"
    
    def __str__(self):
        return f"{self.code} - {self.user}"