from django.db import models
from mixin.models import TimeStampedModel
from . import enums


class Device(TimeStampedModel):
    name = models.CharField(max_length=255)
    device_type = models.CharField(choices=enums.DeviceType.choices, max_length=50)
    # FIXME: Add location later
    # location = PointField()
    serial_number = models.CharField(max_length=255)
    firmware_version = models.CharField(max_length=255, blank=True)
    gpu_model = models.CharField(max_length=255, blank=True)
    status = models.CharField(choices=enums.DeviceStatus.choices, max_length=50, default=enums.DeviceStatus.OFFLINE)

    class Meta:
        db_table = "device"
