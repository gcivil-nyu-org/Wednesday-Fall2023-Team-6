from django.contrib import admin
from .models import User,Patient, HospitalAdmin, Doctor

# Register your models here.
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(HospitalAdmin)
admin.site.register(Doctor)
