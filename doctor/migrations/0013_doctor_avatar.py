# Generated by Django 4.2.5 on 2023-11-03 20:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0012_rename_hospital_doctor_associated_hospital"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/"),
        ),
    ]