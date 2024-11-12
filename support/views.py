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
    
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Your support request has been received. We will get back to you shortly."
        return response
