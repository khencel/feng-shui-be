from rest_framework.viewsets import ModelViewSet

from .models import Chart
from .serializers import ChartSerializer
from .services import ChartService
from utils.response import SuccessResponse
from .selector import ChartSelector


class ChartViewSet(ModelViewSet):

    queryset = Chart.objects.all()
    serializer_class = ChartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chart = ChartService.create_chart(serializer.validated_data)

        return SuccessResponse.create(
            data=self.get_serializer(chart).data,
            message="Chart created successfully",
            status_code=201,
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        chart = ChartService.update_chart(
            instance.id,
            serializer.validated_data,
        )

        return SuccessResponse.create(
            data=self.get_serializer(chart).data,
            message="Chart updated successfully",
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        ChartService.delete_chart(instance.id)

        return SuccessResponse.create(
            message="Chart deleted successfully",
        )
        
    def list(self, request, *args, **kwargs):
        charts = ChartSelector.list_charts()

        serializer = self.get_serializer(charts, many=True)

        return SuccessResponse.create(
            data=serializer.data,
            message="Charts retrieved successfully",
        )
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance)

        return SuccessResponse.create(
            data=serializer.data,
            message="Chart by id retrieved successfully",
        )
        