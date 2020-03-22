from rest_framework import viewsets
from vcfupload_rest.serializers import UploadVcfSerializer
from vcfupload.models import UploadVcf


class UploadVcfViewSet(viewsets.ModelViewSet):
    queryset = UploadVcf.objects.all()
    serializer_class = UploadVcfSerializer
