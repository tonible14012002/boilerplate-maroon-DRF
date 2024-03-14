# Generated by Django 4.2.5 on 2024-01-24 12:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "device_type",
                    models.CharField(choices=[("CAMERA", "Camera")], max_length=50),
                ),
                ("serial_number", models.CharField(max_length=255)),
                ("firmware_version", models.CharField(max_length=255)),
                ("gpu_model", models.CharField(max_length=255)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ACTIVE", "Active"),
                            ("INACTIVE", "Inactive"),
                            ("STAND_BY", "Stand By"),
                            ("ERROR", "Error"),
                            ("OFFLINE", "Offline"),
                        ],
                        default="ACTIVE",
                        max_length=50,
                    ),
                ),
            ],
            options={
                "db_table": "device",
            },
        ),
    ]
