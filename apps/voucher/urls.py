from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VoucherViewSet

router = DefaultRouter()

router.register("voucher", VoucherViewSet, basename="voucher")

urlpatterns = router.urls