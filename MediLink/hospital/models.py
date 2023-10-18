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

class HospitalAppointment(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    reason = models.CharField(max_length=300)
    accebility = models.CharField(max_length=1000, blank=True)
    start_time = models.DateTimeField()
    preferred_doctor = models.ForeignKey('doctor.Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='preferred_doctor')
    status = models.CharField(max_length=50, choices=Choices.appointment_status)