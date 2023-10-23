from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, default="Default Name")


class Doctor(models.Model):
    name = models.CharField(max_length=100, default="Default Name")
    email = models.EmailField(default="example@example.com", unique=True)
    phone = models.CharField(max_length=15, default="000-000-0000")
    sex = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        null=True,
        blank=True,
    )
    specialization = models.CharField(max_length=100)
    associated_hospital = models.CharField(max_length=100)


class Patient(models.Model):
    name = models.CharField(max_length=100, default="Default Name")
    email = models.EmailField(default="example@example.com", unique=True)
    phone = models.CharField(max_length=15, default="000-000-0000")
    sex = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        null=True,
        blank=True,
    )
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)


class HospitalAdmin(models.Model):
    name = models.CharField(max_length=100, default="Default Name")
    email = models.EmailField(default="example@example.com", unique=True)
    phone = models.CharField(max_length=15, default="000-000-0000")
    sex = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        null=True,
        blank=True,
    )
    associated_hospital = models.CharField(max_length=100)

    def __str__(self):
        return self.email
