from apps.charts.models import Chart


class ChartSelector:

    @staticmethod
    def get_chart(chart_id):
        return Chart.objects.get(id=chart_id)

    @staticmethod
    def list_charts():
        return Chart.objects.all()