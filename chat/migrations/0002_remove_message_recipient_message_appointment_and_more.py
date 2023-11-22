# Generated by Django 4.2.4 on 2023-11-22 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0018_alter_doctor_associated_hospital"),
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="recipient",
        ),
        migrations.AddField(
            model_name="message",
            name="appointment",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="doctor.doctorappointment",
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="sender",
            field=models.CharField(
                choices=[("doc", "Doctor"), ("pat", "Patient")], max_length=20
            ),
        ),
    ]
