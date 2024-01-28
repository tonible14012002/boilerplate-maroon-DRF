from django.conf import settings
from django.db import models

from mixin.models import TimeStampedModel

# Create your models here.


class House(TimeStampedModel):
    name = models.CharField(max_length=200, null=False, blank=True)
    description = models.TextField(null=False, blank=True)
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="houses"
    )
    address = models.CharField(max_length=200, null=False, blank=True)

    class Meta:
        db_table = "house"

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
            if value is not None:
                setattr(self, attr_name, value)
        self.save()
        return self


class Room(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="rooms"
    )

    class Meta:
        db_table = "room"
