# Generated by Django 4.2.5 on 2023-09-27 04:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="_nickname",
            field=models.CharField(default="", max_length=100),
        ),
    ]
