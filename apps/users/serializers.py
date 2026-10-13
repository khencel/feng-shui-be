from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "gender",
            "date_of_birth",
            "is_active"
        ]
        extra_kwargs = {
            "password" : {
                "write_only": True,
                "required":False
            }
        }
        
    def create(self, validate_data):
        password = validate_data.pop("password", None)
        
        if not password:
            password = "testPassword"
        
        user = User(**validate_data)
        
        if password:
            user.set_password(password)
           
            user.save()
            user.google_id = user.id
            user.save(update_fields=["google_id"])

            return user
        
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
            
        instance.save()
        
        return instance
        