from rest_framework import serializers
from .models import Combination

class CombinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combination
        fields = "__all__"