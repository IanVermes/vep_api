import pathlib
import io
import typing as t

from django.core.files import File
from rest_framework import serializers

from webvep_api.forms import VcfForm
from helpers import vcf_helpers


class PingSerializer(serializers.Serializer):
    """Serializer for JSON fields"""

    data = serializers.CharField(required=True)

    def validate_data(self, value):
        """Check that the data field is specific value."""
        if value != "ping":
            raise serializers.ValidationError("field must be `ping`")
        return value


class VcfSerializer(serializers.Serializer):
    """Serializer for JSON fields"""

    vcf_file = serializers.FileField(required=True)

    def validate_vcf_file(self, value):
        filename = pathlib.Path(value.name)
        if filename.suffix != ".vcf":
            raise serializers.ValidationError(
                "Invalid file: wrong extension, expected .vcf"
            )
        if not self._has_binomial_name(filename.name):
            raise serializers.ValidationError(
                "Invalid file: wrong name, expect binomial species name"
            )
        return value

    def _has_binomial_name(self, filename: str) -> bool:
        binomial_name = vcf_helpers.extract_binomial_name(filename)
        return binomial_name in vcf_helpers.BINOMIAL_NAMES

    def create(self, validate_data):
        memory_file = validate_data["vcf_file"]

        filename = pathlib.Path(memory_file.name).name
        with memory_file.open("rb"):
            vcf_content = memory_file.read()
        return VcfForm(filename=filename, content=vcf_content)
