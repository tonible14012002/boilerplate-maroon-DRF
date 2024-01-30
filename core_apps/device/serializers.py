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
    """
    Create Device given `room_id`
    Update device
    View Device detail
    """

    specification = RDeiviceSpecDetail(read_only=True)
    room_id = serializers.UUIDField(write_only=True)
    room = serializers.UUIDField(source="room.id", read_only=True)
    specification_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Device
        fields = [
            "id",
            "name",
            "room_id",
            "room",  # should not detail, only id
            "specification",
            "device_type",
            "serial_number",
            "created_at",
            "updated_at",
            "status",  # should be read only
            "specification_id",
            # NOTE: secret must not be exposed
        ]
        read_only_fields = [
            "status",
            "device_type",
        ]
        # custome fields
        no_update_fields = [
            "specification_id",
            "name",
            "device_type",
            "room",
        ]

    def update(self, instance, validated_data):
        device = instance
        room_id = validated_data.pop("room_id", None)
        name = validated_data.get("name", None)
        return device.update(name=name, room_id=room_id)

    def create(self, validated_data):
        room_id = validated_data.pop("room_id")
        spec_id = validated_data.pop("specification_id")
        return models.Device.create_new_for_room(
            room_id=room_id,
            spec_id=spec_id,
            name=validated_data.get("name", ""),
            device_type=validated_data.get("device_type", ""),
            serial_number=validated_data.get("serial_number", ""),
        )
