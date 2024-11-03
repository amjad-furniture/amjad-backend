from categories.models import Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:    
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("The name field cannot be empty.")
        if not value.isalnum():
            raise serializers.ValidationError("The name field can only contain letters and numbers.")
        return value