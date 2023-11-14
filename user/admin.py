from django.contrib import admin
from .models import Patient, Hospital_Reviews, Doctor_Reviews


# Register your models here.
admin.site.register(Patient)
admin.site.register(Hospital_Reviews)
admin.site.register(Doctor_Reviews)
