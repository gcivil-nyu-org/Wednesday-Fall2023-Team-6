from django.db import models
from user.models import User


class Choices:
    appointment_status = [
        ("REQ", "Requested"),
        ("CNF", "Confirmed"),
        ("CCL", "Cancelled"),
        ("REJ", "Rejected"),
    ]


class Doctor(User):
    primary_speciality = models.CharField(max_length=50)
    associated_hospital = models.ForeignKey(
        "hospital.Hospital",
        max_length=100,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )


class DoctorAppointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey("user.Patient", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    name = models.CharField(max_length=100, default="Default Name")
    phone = models.CharField(max_length=15, default="Default Phone")
    email = models.EmailField(max_length=254, default="example@example.com")
    reason = models.CharField(max_length=300, default="Default Reason")
    status = models.CharField(max_length=50, choices=Choices.appointment_status)
    cancel_msg = models.CharField(max_length=100, null=True, blank=True)
