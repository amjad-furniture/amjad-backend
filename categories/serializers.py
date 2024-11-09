from rest_framework import serializers
from .models import Category
from dynamic_rest.serializers import DynamicModelSerializer

class CategorySerializer(DynamicModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Category name is required.")
        if len(value) < 3:
            raise serializers.ValidationError("Category name must be at least 3 characters long.")
        return value