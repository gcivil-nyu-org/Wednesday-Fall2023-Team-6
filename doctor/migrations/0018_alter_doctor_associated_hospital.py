# Generated by Django 4.2.4 on 2023-11-11 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("hospital", "0014_hospitaladmin_active_status"),
        ("doctor", "0017_doctor_active_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="associated_hospital",
            field=models.ForeignKey(
                blank=True,
                max_length=100,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="hospital.hospital",
            ),
        ),
    ]
