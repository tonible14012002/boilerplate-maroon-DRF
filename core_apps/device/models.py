from django.db import models
from mixin.models import TimeStampedModel
from . import enums, managers
from core_apps.house import models as house_models
from django.shortcuts import get_object_or_404
from utils import random as random_utils


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

    objects = managers.DeviceManager()

    class Meta:
        db_table = "device"

    # ----- Factory ------
    @classmethod
    def create_new_for_room(
        cls, room_id, spec_id, name, device_type, serial_number
    ):
        try:
            room = house_models.Room.objects.get(id=room_id)
            specification = DeviceSpec.objects.get(id=spec_id)
        except house_models.Room.DoesNotExist as e:
            print(e, flush=True)
            raise Exception("Room does not exist")
        return cls.objects.create(
            room=room,
            specification=specification,
            secret=random_utils.id_generator(10),
            status=enums.DeviceStatus.OFFLINE,
            name=name,
            device_type=device_type,
            serial_number=serial_number,
        )

    # ----- Queries ------
    @classmethod
    def get_room_devices(cls, room_id):
        return cls.objects.filter_by_room_id(room_id)

    @classmethod
    def get_house_devices(cls, house_id):
        house = get_object_or_404(house_models.House, id=house_id)
        return cls.objects.filter(room__house=house)

    # ------- Mutators -------
    def update(self, name, room_id):
        if room_id:
            room = get_object_or_404(house_models.Room, id=room_id)
            self.room = room
        if name is not None:
            self.name = name
        self.save()
        return self
