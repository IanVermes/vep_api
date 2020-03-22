from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [path(r"", include(router.urls))]
