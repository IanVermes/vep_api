from rest_framework import serializers


class PingSerializer(serializers.Serializer):
    """Serializer for JSON fields"""

    data = serializers.CharField(required=True)

    def validate_data(self, value):
        """Check that the data field is specific value."""
        if value != "ping":
            raise serializers.ValidationError("field must be `ping`")
        return value
