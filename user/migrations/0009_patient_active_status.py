# Generated by Django 4.2.3 on 2023-11-09 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_patient_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='active_status',
            field=models.BooleanField(default=True),
        ),
    ]
