from django.db import models


class Choices:
    senders = [("doc", "Doctor"), ("pat", "Patient")]


class Message(models.Model):
    appointment = models.ForeignKey(
        "doctor.DoctorAppointment", on_delete=models.CASCADE, null=True
    )
    sender = models.CharField(max_length=20, choices=Choices.senders)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to="attachments/", null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} {self.appointment}"
