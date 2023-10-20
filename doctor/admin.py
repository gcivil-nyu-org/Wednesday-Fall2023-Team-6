from django.contrib import admin

from .models import Doctor, DoctorAppointment

# Register your models here.
admin.site.register(Doctor)
admin.site.register(DoctorAppointment)
