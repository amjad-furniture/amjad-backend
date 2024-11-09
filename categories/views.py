from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer
from dynamic_rest.viewsets import DynamicModelViewSet


class CategoryViewSet(DynamicModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer