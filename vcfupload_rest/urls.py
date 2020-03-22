from django.urls import path, include
from rest_framework import routers

from vcfupload_rest.viewsets import UploadVcfViewSet

router = routers.DefaultRouter()
router.register("vcfs", UploadVcfViewSet, "vcfs")

urlpatterns = [path(r"", include(router.urls))]
