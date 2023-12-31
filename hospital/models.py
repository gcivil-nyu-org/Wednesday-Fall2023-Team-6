from django.db import models

from user.models import User


class Choices:
    boroughs = [
        ("BKN", "Brooklyn"),
        ("MHT", "Manhattan"),
        ("QNS", "Queens"),
        ("BRX", "Bronx"),
        ("SND", "Staten Island"),
    ]

    appointment_status = [
        ("REQ", "Requested"),
        ("CNF", "Confirmed"),
        ("CCL", "Cancelled"),
        ("REJ", "Rejected"),
    ]


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    facility_type = models.CharField(max_length=100)
    borough = models.CharField(max_length=50, choices=Choices.boroughs)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=200)
    postal_code = models.IntegerField()
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.name

    def filter_ratings(self, rating_filter):
        if rating_filter == "0":
            return self.filter_reviews(min_rating=0)
        elif rating_filter == "1":
            return self.filter_reviews(min_rating=2)
        elif rating_filter == "2":
            return self.filter_reviews(min_rating=3)
        elif rating_filter == "3":
            return self.filter_reviews(min_rating=4)
        elif rating_filter == "4":
            return self.filter_reviews(min_rating=5)
        else:
            return self.all()

    def filter_reviews(self, min_rating):
        return self.annotate(avg_rating=models.Avg("hospital_reviews__rating")).filter(
            avg_rating__gte=min_rating
        )


class HospitalAdmin(User):
    associated_hospital = models.ForeignKey(
        "hospital.Hospital", max_length=100, null=True, on_delete=models.CASCADE
    )


class HospitalAppointment(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    patient = models.ForeignKey("user.Patient", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    reason = models.CharField(max_length=300)
    accebility = models.CharField(max_length=1000, blank=True)
    start_time = models.DateTimeField()
    preferred_doctor = models.ForeignKey(
        "doctor.Doctor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="preferred_doctor",
    )
    status = models.CharField(max_length=50, choices=Choices.appointment_status)
    cancel_msg = models.CharField(max_length=100, null=True, blank=True)
