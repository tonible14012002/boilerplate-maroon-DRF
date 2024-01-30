from django.db import models


class DeviceManager(models.Manager):
    def filter_by_room_id(self, room_id):
        return self.get_queryset().filter(room__id=room_id)
