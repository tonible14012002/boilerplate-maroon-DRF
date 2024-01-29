from rest_framework import serializers
from . import models
from core_apps.house import serializers as house_serializers
from mixin.serializers import NoUpdateSerializer


class RDeiviceSpecDetail(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceSpec
        fields = [
            "id",
            "name",
            "series_name",
            "gpu",
            "gpu_max_fre",
            "cpu",
            "cpu_max_fre",
            "vision_acceleration",
            "storage",
            "memory",
            "power",
        ]


class CRUDevice(serializers.ModelSerializer, NoUpdateSerializer):
    specification = RDeiviceSpecDetail(read_only=True)

    class Meta:
        model = models.Device
        fields = [
            "id",
            "name",
            "room",  # should not detail, only id
            "sepcification",
            "device_type",
            "serial_number",
            "created_at",
            "updated_at",
            "status",  # should be read only
            # NOTE: secret must not be exposed
        ]
        read_only_fields = [
            "status",
            "device_type",
        ]

        # custome fields
        no_update_fields = [
            "name",
            "device_type",
        ]
