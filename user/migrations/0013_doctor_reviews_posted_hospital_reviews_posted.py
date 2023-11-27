# Generated by Django 4.2.4 on 2023-11-15 14:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0012_rename_doctor_doctor_reviews_doctor_name_doctor"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor_reviews",
            name="posted",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 11, 15, 9, 0, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AddField(
            model_name="hospital_reviews",
            name="posted",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 11, 15, 9, 0, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]