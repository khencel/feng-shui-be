from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id          =   models.AutoField(primary_key=True)
    google_id   =   models.CharField(max_length=50, unique=True)
    email       =   models.EmailField(max_length=100, unique=True)
    is_admin    =   models.BooleanField(default=False)
    first_name  =   models.CharField(max_length=100)
    last_name   =   models.CharField(max_length=100)
    gender      =   models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True,blank=True)
    is_active   =   models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    