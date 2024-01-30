from django.db import models


class HouseManager(models.Manager):
    def filter_by_owner_id(self, user_id):
        return self.get_queryset().filter(owners__id=user_id)


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
