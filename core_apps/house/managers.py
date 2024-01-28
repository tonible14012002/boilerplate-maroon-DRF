from typing import Any

from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.query import QuerySet


class RoomBasicManager(models.Manager):
    def from_ids(self, *ids):
        return self.filter(id__in=ids)

    def order_by_age(self, ascendent=False):
        if ascendent:
            return self.get_queryset().order_by("created_at")
        else:
            return self.get_queryset().order_by("-created_at")

    def from_house_id(self, house_id):
        return self.filter(house__id=house_id).order_by("-created_at")
