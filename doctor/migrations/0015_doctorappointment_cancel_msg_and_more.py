# Generated by Django 4.2.5 on 2023-11-09 16:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0014_alter_doctor_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctorappointment",
            name="cancel_msg",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="doctorappointment",
            name="status",
            field=models.CharField(
                choices=[
                    ("REQ", "Requested"),
                    ("CNF", "Confirmed"),
                    ("CCL", "Cancelled"),
                    ("REJ", "Rejected"),
                ],
                max_length=50,
            ),
        ),
    ]