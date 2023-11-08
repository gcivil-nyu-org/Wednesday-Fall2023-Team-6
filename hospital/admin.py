from django.contrib import admin
from .models import Hospital, HospitalAppointment, HospitalAdmin

# Register your models here.
admin.site.register(Hospital)
admin.site.register(HospitalAdmin)
admin.site.register(HospitalAppointment)
