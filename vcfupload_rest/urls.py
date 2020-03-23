from django.urls import path, include

# from rest_framework import routers

# from vcfupload_rest.viewsets import UploadVcfViewSet

# router = routers.DefaultRouter()
# router.register("vcfs", UploadVcfViewSet, "vcfs")
from rest_framework.urlpatterns import format_suffix_patterns
from vcfupload_rest.views import vcf_detail, vcf_list

urlpatterns = [path("vcfs/", vcf_list), path("vcfs/<int:pk>", vcf_detail)]

urlpatterns = format_suffix_patterns(urlpatterns)
