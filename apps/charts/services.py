from django.db import transaction
from .models import Chart

class ChartService:
    @staticmethod
    @transaction.atomic
    def create_chart(data):
        chart = Chart.objects.create(**data)
        return chart

    @staticmethod
    @transaction.atomic
    def update_chart(chart_id, data):
        chart = Chart.objects.get(id=chart_id)
        for key, value in data.items():
            setattr(chart, key, value)
        chart.save()
        return chart

    @staticmethod
    @transaction.atomic
    def delete_chart(chart_id):
        chart = Chart.objects.get(id=chart_id)
        chart.delete()