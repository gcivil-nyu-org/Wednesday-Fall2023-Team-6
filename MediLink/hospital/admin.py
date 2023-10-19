from django.contrib import admin
from .models import Hospital, HospitalAppointment

# Register your models here.
admin.site.register(Hospital)
admin.site.register(HospitalAppointment)
