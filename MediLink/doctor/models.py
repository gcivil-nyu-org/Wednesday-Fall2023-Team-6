from django.db import models

class Choices:
    boroughs = [
        ("BKN", "Brooklyn"), 
        ("MHT", "Manhattan"), 
        ("QNS", "Queens"), 
        ("BRX", "Bronx"), 
        ("SND", "Staten Island")
    ]
    
    appointment_status = [
        ("REQ", "Requested"),
        ("CNF", "Confirmed"),
        ("CCL", "Cancelled")
    ]

class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    practice_name = models.CharField(max_length=100)
    primary_speciality = models.CharField(max_length=50)
    site_name = models.CharField(max_length=100)
    practice_borough = models.CharField(max_length=50)  # Assuming boroughs are similar to the hospital model
    practice_mailing_address = models.CharField(max_length=200)
    practice_phone_number = models.CharField(max_length=12)
    organization_type = models.CharField(max_length=100)
    practice_zip_code = models.IntegerField()

class DoctorAppointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=Choices.appointment_status)

