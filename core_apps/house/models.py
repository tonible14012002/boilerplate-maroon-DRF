from django.conf import settings
from django.db import models
from . import managers
from mixin.models import TimeStampedModel

# Create your models here.


class House(TimeStampedModel):
    name = models.CharField(max_length=200, null=False, blank=True)
    description = models.TextField(null=False, blank=True)
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="houses"
    )
    address = models.CharField(max_length=200, null=False, blank=True)
    objects = managers.HouseManager()

    class Meta:
        db_table = "house"

    # ----- Queries -----
    @classmethod
    def get_owned_house(cls, user_id):
        return cls.objects.filter_by_owner_id(user_id)

    # ----- Property -----
    def is_user_owner(self, user):
        return self.owners.filter(pk=user.pk).exists()

    # ----- Factory -----
    @classmethod
    def create_new(cls, owners, name, description, address):
        house = cls.objects.create(
            name=name, description=description, address=address
        )
        house.owners.set(*owners)
        return house

    # ----- Mutator -----
    def update(self, name, description, address):
        values = [name, description, address]
        attr_names = ["name", "description", "address"]

        for value, attr_name in zip(values, attr_names):
            if value is not None:  # NOTE empty string is still allow
                setattr(self, attr_name, value)
        self.save()
        return self


class Room(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=False, blank=True)
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="rooms"
    )
    objects = managers.RoomBasicManager()

    class Meta:
        db_table = "room"

    # ----- Property -----

    # ----- Factory -----
    @classmethod
    def create_new(cls, house, name, description):
        return cls.objects.create(
            house=house, name=name, description=description
        )

    # ----- Mutator -----
    def update(self, name, description):
        values = [name, description]
        attr_names = ["name", "description"]

        for value, attr_name in zip(values, attr_names):
            if value is not None:  # NOTE empty string is still allow
                setattr(self, attr_name, value)

        self.save()
        return self
