from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Support
from .serializers import SupportSerializer

class SupportViewSet(viewsets.ModelViewSet):
    """
    Support ViewSet.
    """
    queryset = Support.objects.all()
    serializer_class = SupportSerializer
    permission_classes = [AllowAny]
