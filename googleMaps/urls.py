from django.urls import path
from . import views

app_name = "googleMaps"

urlpatterns = [
    path("map/", views.map, name="map"),
]
