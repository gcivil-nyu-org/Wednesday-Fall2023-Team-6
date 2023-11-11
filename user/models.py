from django.db import models


class Choices:
    boroughs = [
        ("BKN", "Brooklyn"),
        ("MHT", "Manhattan"),
        ("QNS", "Queens"),
        ("BRX", "Bronx"),
        ("SND", "Staten Island"),
    ]

    sex = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]


class User(models.Model):
    name = models.CharField(max_length=100, default="Default Name")
    email = models.EmailField(default="example@example.com", unique=True)
    phone = models.CharField(max_length=15, default="000-000-0000")
    sex = models.CharField(max_length=10, choices=Choices.sex, null=True, blank=True)

    address = models.CharField(max_length=200)
    borough = models.CharField(max_length=50, choices=Choices.boroughs)

    zip = models.IntegerField()

    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/default-avatar.png",
        null=True,
        blank=True,
    )
    
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " (" + self.email + ")"

    class Meta:
        abstract = True


class Patient(User):
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
