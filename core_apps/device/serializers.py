from rest_framework import serializers
from . import models
from mixin.serializers import NoUpdateSerializer
from core_apps.user import serializers as user_serializers


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
    include 'room' instance in context
    Update device
    View Device detail
    """

    specification = RDeiviceSpecDetail(read_only=True)
    room = serializers.UUIDField(source="room.id", read_only=True)
    specification_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Device
        fields = [
            "id",
            "name",
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
        name = validated_data.get("name", None)
        return device.update(name=name)

    def create(self, validated_data):
        room = self.context.get("room")
        spec_id = validated_data.pop("specification_id")
        return models.Device.create_new_for_room(
            room=room,
            spec_id=spec_id,
            name=validated_data.get("name", ""),
            device_type=validated_data.get("device_type", ""),
            serial_number=validated_data.get("serial_number", ""),
        )


class RDeviceDetail(CRUDevice):
    related_users = user_serializers.ReadBasicUserProfile(
        source="get_room_users", many=True, read_only=True
    )

    class Meta(CRUDevice.Meta):
        fields = CRUDevice.Meta.fields + ["related_users"]
