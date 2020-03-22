from rest_framework import serializers
from vcfupload.models import UploadVcf


class UploadVcfSerializer(serializers.ModelSerializer):
    """Convert the uploaded file back and forth between Python DB model and JSON"""

    class Meta:
        model = UploadVcf
        fields = ("pk", "file", "original_filename")
