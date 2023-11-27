# Generated by Django 4.2.4 on 2023-11-17 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0019_alter_doctor_associated_hospital"),
        ("hospital", "0014_hospitaladmin_active_status"),
        ("user", "0014_rename_likes_doctor_reviews_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor_reviews",
            name="doctor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="doctor.doctor"
            ),
        ),
        migrations.AlterField(
            model_name="hospital_reviews",
            name="hospital",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hospital.hospital"
            ),
        ),
    ]