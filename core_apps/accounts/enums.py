from django.db import models


class Gender(models.TextChoices):
    Male = ('MALE', 'Male')
    Female = ('FEMALE', 'Female')
    Other = ('OTHER', 'Other')
