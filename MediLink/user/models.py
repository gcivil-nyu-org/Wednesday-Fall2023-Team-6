from django.db import models

from django.db import models


class User(models.Model):
      name = models.CharField(max_length=100, default='Default Name')
      email = models.EmailField(default='example@example.com', unique=True)
      password = models.CharField(max_length=100)
      phone = models.CharField(max_length=15, default='000-000-0000')
      sex = models.CharField(
            max_length=10,
            choices=[
                  ('male', 'Male'),
                  ('female', 'Female'),
                  ('other', 'Other')
            ],
          null=True,
          blank=True
      )

      # User type and related fields
      USER_TYPE_CHOICES = [
            ('patient', 'General Patient'),
            ('doctor', 'Doctor / Medical Specialist'),
            ('hospital-admin', 'Hospital Administrator'),
      ]
      user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='patient')

      # Additional fields for Doctors
      specialization = models.CharField(max_length=100, blank=True, null=True)

      # Fields for Hospital Administrator and Doctors
      associated_hospital = models.CharField(max_length=100, blank=True, null=True)

      # Additional fields for Patient
      insurance_provider = models.CharField(max_length=100, blank=True, null=True)

      def __str__(self):
            return self.email
