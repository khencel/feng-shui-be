from rest_framework import serializers
from .models import Chart


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = [
            "id",
            "door_location",
            "house_facing",
            "se",
            "s",
            "sw",
            "e",
            "w",
            "ne",
            "n",
            "nw",
            "number",
            "lead_stem",
            "house_stem_branch",
            "facing",
            "backing",
            "created_at",
            "updated_at"
        ]

    