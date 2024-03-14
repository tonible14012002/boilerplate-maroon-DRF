from django.db import models


class DeviceType(models.TextChoices):
    CAMERA = ('CAMERA', 'Camera')


class DeviceStatus(models.TextChoices):
    ACTIVE = ('ACTIVE', 'Active')
    INACTIVE = ('INACTIVE', 'Inactive')
    STAND_BY = ('STAND_BY', 'Stand By')
    ERROR = ('ERROR', 'Error')
    OFFLINE = ('OFFLINE', 'Offline')
    # ...
