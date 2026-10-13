
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.authentication import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path(
        "api/login/",
        CustomTokenObtainPairView.as_view(),
        name="token",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    
    path("api/", include("apps.users.urls")),
    path("api/", include("apps.charts.urls")),
    path("api/", include("apps.payments.urls")),
    path("api/", include("apps.voucher.urls")),
]
