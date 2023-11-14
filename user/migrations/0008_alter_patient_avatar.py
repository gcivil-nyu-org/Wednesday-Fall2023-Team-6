# Generated by Django 4.2.4 on 2023-11-07 19:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0007_patient_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="avatars/default-avatar.png",
                null=True,
                upload_to="avatars/",
            ),
        ),
    ]
