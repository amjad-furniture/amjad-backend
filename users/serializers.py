from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth import password_validation
from dynamic_rest.serializers import DynamicModelSerializer
from .models import User




class UserSerializer(DynamicModelSerializer):
    """
    Serializer for User.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "phone_number",
        ]


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for User Login.
    """

    username = serializers.CharField(max_length=15)
    password = serializers.CharField(required=True, write_only=True)


class EmptySerializer(serializers.Serializer):
    """
    Serializer for empty response.
    """

    pass


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for change password
    it check current and new password.
    """

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
