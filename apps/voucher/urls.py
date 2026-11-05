from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VoucherViewSet, CheckVoucherIfValid

router = DefaultRouter()

router.register("voucher", VoucherViewSet, basename="voucher")

urlpatterns = router.urls + [
    path(
        "vouchers/check-voucher/",
        CheckVoucherIfValid.as_view(),
        name="check-voucher-valid"
    ),
]