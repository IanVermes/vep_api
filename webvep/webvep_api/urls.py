from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from webvep_api.views import ping


urlpatterns = [path("ping/", ping)]
urlpatterns = format_suffix_patterns(urlpatterns)
