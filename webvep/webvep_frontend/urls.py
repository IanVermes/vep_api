from django.urls import path, include

from webvep_frontend import views

urlpatterns = [path("", views.home), path("upload", views.simple_upload)]
