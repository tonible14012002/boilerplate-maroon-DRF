from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid


# Create your models here.
class MyUser(AbstractUser):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    dob = models.DateField(null=True)
    phone = PhoneNumberField()

    REQUIRED_FIELDS = ["email", "last_name", "first_name"]
