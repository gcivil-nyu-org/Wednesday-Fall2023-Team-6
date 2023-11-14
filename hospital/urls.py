from django.urls import path

from . import views

app_name = "hospital"

urlpatterns = [
    path("", views.HospitalListView.as_view(), name="list_view"),
    path("autocomplete/", views.autocomplete_hospitals, name="autocomplete_hospitals"),
    path("<int:pk>/", views.HospitalDetailView.as_view(), name="detail_view"),
    path(
        "<int:hospital_id>/bookAppointment",
        views.book_appointment,
        name="book_appointment",
    ),
    path("addHospitalReview/", views.add_review, name="add_review"),
]
