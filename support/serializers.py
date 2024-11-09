from rest_framework import serializers
from .models import Support


class SupportSerializer(serializers.ModelSerializer):
    """
    Serializer for Support.
    """

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Support
        fields = [
            "id",
            'name',
            'email',
            "phone_number",
            "message",
            "created_at",
        ]
