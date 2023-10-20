from django.db import models


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
    ]


class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    primary_speciality = models.CharField(max_length=50)
    hospital = models.ForeignKey(
        "hospital.Hospital", max_length=100, null=True, on_delete=models.SET_NULL
    )
    borough = models.CharField(max_length=50, choices=Choices.boroughs)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    zip = models.IntegerField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class DoctorAppointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    name = models.CharField(max_length=100, default="Default Name")
    phone = models.CharField(max_length=15, default="Default Phone")
    email = models.EmailField(max_length=254, default="example@example.com")
    reason = models.CharField(max_length=300, default="Default Reason")
    status = models.CharField(max_length=50, choices=Choices.appointment_status)
