from django.urls import path

from hospital.views import TempDetails, get_hospitals
from . import views

app_name = "hospital"

urlpatterns = [
    path("", views.HospitalListView.as_view(), name="list_view"),
    path("<int:pk>/", views.HospitalDetailView.as_view(), name="detail_view"),
    path(
        "<int:hospital_id>/bookAppointment",
        views.book_appointment,
        name="book_appointment",
    ),
    path("details/", TempDetails, name="details"),
    path("get_hospitals/", get_hospitals, name="get_hospitals"),
]
