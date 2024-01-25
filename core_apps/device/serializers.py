from rest_framework import serializers
from . import models


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = ['id', 'name', 'device_type', 'serial_number',
                  'firmware_version', 'gpu_model', 'status', 'created_at', 'updated_at']
        extra_kwargs = {
            'firmware_version': {'required': False},
            'gpu_model': {'required': False},
        }
        read_only_fields = ['id', 'created_at', 'updated_at', 'status']

        # custome fields
        no_update_fields = ['name', 'device_type', 'serial_number']
