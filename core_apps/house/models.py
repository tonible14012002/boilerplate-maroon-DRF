from django.db import models
from django.conf import settings
from mixin.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class House(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='houses')
    address = models.CharField(max_length=200)
    class Meta:
        db_table = 'house'


class Room(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='rooms')

    class Meta:
        db_table = 'room'
