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
    
class Hospital(models.Model):
    facility_type = models.CharField(max_length=100)
    borough = models.CharField(max_length=50, choices=Choices.boroughs)
    phone = models.CharField(max_length=12)
    location = models.CharField(max_length=200)
    postal_code = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    nta = models.CharField(max_length=100)

class HospitalAppointment(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    preferred_doctor = models.ForeignKey('doctor.Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='preferred_doctor')
    assigned_doctor = models.ForeignKey('doctor.Doctor', on_delete=models.CASCADE, null=True, blank=True, related_name='assigned_doctor')
    status = models.CharField(max_length=50, choices=Choices.appointment_status)