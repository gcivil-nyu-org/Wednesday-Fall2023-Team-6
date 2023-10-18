# Generated by Django 4.2.4 on 2023-10-18 01:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0003_rename_practice_mailing_address_doctor_address_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="borough",
            field=models.CharField(
                choices=[
                    ("BKN", "Brooklyn"),
                    ("MHT", "Manhattan"),
                    ("QNS", "Queens"),
                    ("BRX", "Bronx"),
                    ("SND", "Staten Island"),
                ],
                max_length=50,
            ),
        ),
    ]