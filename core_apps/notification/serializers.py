from rest_framework import serializers
from . import models


class RNotification(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = [
            "id",
            "user",
            "house",
            "room",
            "label",
            "description",
            "event_code",
            "meta",
        ]
