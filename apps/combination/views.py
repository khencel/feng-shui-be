from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import Combination, CombinationSerializer

class CombinationViewSet(ModelViewSet):
    queryset = Combination.objects.all()
    serializer_class = CombinationSerializer
    permission_classes = [IsAuthenticated]
