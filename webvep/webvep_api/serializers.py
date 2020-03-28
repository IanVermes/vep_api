from rest_framework import serializers


class PingSerializer(serializers.Serializer):
    """Serializer for JSON fields"""

    data = serializers.CharField()

