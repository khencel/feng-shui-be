from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CombinationViewSet

router = DefaultRouter()

router.register("combination", CombinationViewSet, basename="combination")

urlpatterns = router.urls + [
   
]