from rest_framework.routers import DefaultRouter

from .views import ChartViewSet

router = DefaultRouter()

router.register("charts", ChartViewSet, basename="charts")

urlpatterns = router.urls