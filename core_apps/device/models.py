from django.db import models
from mixin.models import TimeStampedModel
from drf_extra_fields import PointField
from . import enums

# Create your models here.
# PointField accept json
#   {
#     "location":{
#         "latitude": 37.0625
#         "longitude": -95.677068,
#     }
#   }


class Device(TimeStampedModel):
    name = models.CharField(max_length=255)
    device_type = models.CharField(choices=enums.DeviceType, max_length=50)
    location = PointField()
    serial_number = models.CharField(max_length=255)
    firmware_version = models.CharField(max_length=255)
    gpu_model = models.CharField(max_length=255)
    status = models.CharField(choices=enums.DeviceStatus, max_length=50)

    class Meta:
        db_table = "device"
