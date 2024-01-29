from django.db import models
from mixin.models import TimeStampedModel
from . import enums
from core_apps.house import models as house_models


class DeviceSpec(models.Model):
    name = models.CharField(max_length=255)
    series_name = models.CharField(max_length=255)
    gpu = models.CharField(max_length=255)
    gpu_max_fre = models.CharField(max_length=50)
    cpu = models.CharField(max_length=255)
    cpu_max_fre = models.CharField(max_length=50)
    vision_acceleration = models.CharField(max_length=255)
    storage = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)
    power = models.CharField(max_length=255)

    class Meta:
        db_table = "device_spec"
        unique_together = ["name", "series_name"]


class Device(TimeStampedModel):
    specification = models.ForeignKey(
        DeviceSpec,
        on_delete=models.SET_NULL,
        null=True,
        related_name="devices",
    )
    room = models.ForeignKey(
        house_models.Room,
        on_delete=models.SET_NULL,
        related_name="devices",
        null=True,
    )
    name = models.CharField(max_length=255)
    device_type = models.CharField(
        choices=enums.DeviceType.choices, max_length=50
    )
    serial_number = models.CharField(max_length=255)
    secret = models.CharField(max_length=100, blank=False)
    status = models.CharField(
        choices=enums.DeviceStatus.choices,
        max_length=50,
        default=enums.DeviceStatus.OFFLINE,
    )

    class Meta:
        db_table = "device"
