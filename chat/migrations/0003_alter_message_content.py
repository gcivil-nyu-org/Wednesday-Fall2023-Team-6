# Generated by Django 4.2.4 on 2023-11-22 02:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0002_remove_message_recipient_message_appointment_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="content",
            field=models.TextField(blank=True),
        ),
    ]
