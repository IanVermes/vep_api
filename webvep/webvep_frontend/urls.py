from django.urls import path, include

from webvep.webvep_frontend import views

urlpatterns = [
    path("", views.home),
]
