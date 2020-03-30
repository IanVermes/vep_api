from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from webvep_api.views import ping_view, vcf_view, vep_view

urlpatterns = [path("ping/", ping_view), path("vcf/", vcf_view), path("vep/", vep_view)]
urlpatterns = format_suffix_patterns(urlpatterns)
