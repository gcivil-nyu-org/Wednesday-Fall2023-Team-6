from django.urls import path
from . import views

urlpatterns = [
    path("doctorMap/", views.doctor_map, name="doctor_map"),
]
