from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import GoogleLoginView, UserViewSet, TestApi

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    *router.urls,
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
    path("test", TestApi.as_view(), name="test-api"),
]