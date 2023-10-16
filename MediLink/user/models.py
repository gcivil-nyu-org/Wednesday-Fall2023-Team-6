from django.db import models

class User(models.Model):
      email = models.EmailField(default='example@example.com', unique=True)
      password = models.CharField(max_length=100, default='example@example.com')
