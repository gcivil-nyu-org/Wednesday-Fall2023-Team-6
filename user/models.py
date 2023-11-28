from django.db import models
from datetime import datetime
import pytz


class Choices:
    boroughs = [
        ("BKN", "Brooklyn"),
        ("MHT", "Manhattan"),
        ("QNS", "Queens"),
        ("BRX", "Bronx"),
        ("SND", "Staten Island"),
    ]

    sex = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]


class User(models.Model):
    name = models.CharField(max_length=100, default="Default Name")
    email = models.EmailField(default="example@example.com", unique=True)
    phone = models.CharField(max_length=15, default="000-000-0000")
    sex = models.CharField(max_length=10, choices=Choices.sex, null=True, blank=True)

    address = models.CharField(max_length=200)
    borough = models.CharField(max_length=50, choices=Choices.boroughs)

    zip = models.IntegerField()

    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/default-avatar.png",
        null=True,
        blank=True,
    )

    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " (" + self.email + ")"

    class Meta:
        abstract = True


class Patient(User):
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)


class Doctor(User):
    primary_speciality = models.CharField(max_length=50)
    associated_hospital = models.ForeignKey(
        "hospital.Hospital",
        max_length=100,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="user_doctors",
    )


class Hospital_Reviews(models.Model):
    hospital = models.ForeignKey("hospital.Hospital", on_delete=models.CASCADE)
    review_from = models.CharField(max_length=100)
    rating = models.PositiveIntegerField()
    title = models.TextField()
    description = models.TextField()
    posted = models.DateTimeField(
        default=datetime(2023, 11, 15, 9, 0, 0, 0, tzinfo=pytz.UTC)
    )

    def __str__(self):
        return f"Review for {self.hospital} by {self.review_from}"


class Doctor_Reviews(models.Model):
    doctor = models.ForeignKey("doctor.Doctor", on_delete=models.CASCADE)
    review_from = models.CharField(max_length=255)
    rating = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    posted = models.DateTimeField(
        default=datetime(2023, 11, 15, 9, 0, 0, 0, tzinfo=pytz.UTC)
    )

    def __str__(self):
        return f"Review for {self.doctor} by {self.review_from}"
