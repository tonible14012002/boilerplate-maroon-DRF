import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from mixin.models import TimeStampedModel

from . import enums, managers


# Create your models here.
class MyUser(AbstractUser):
    REQUIRED_FIELDS = ["email", "last_name", "first_name"]

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    dob = models.DateField(null=True)
    phone = PhoneNumberField()
    is_test = models.BooleanField(default=False)

    objects = managers.UserManager()
    tests = managers.TestUserManager()

    class Meta:
        db_table = "user"

    # --------------- FACTORY --------------- #

    @classmethod
    def create_register(
        cls,
        *,
        username: str,
        password: str,
        extra_fields: dict,
        profile_fields: dict,
        is_test=False
    ):
        # NOTE: Use this method for create new user instead of objects.create()
        if is_test:
            factory = cls.tests.create
        else:
            factory = cls.objects.create
        user = factory(username=username, password=password, **extra_fields)
        Profile.objects.create(user=user, **profile_fields)
        return user

    # --------------- PROPERTIES --------------- #

    # --------------- MUTATORS --------------- #

    def update_field(self, *, first_name, last_name, dob, phone):
        values = [first_name, last_name, dob, phone]
        attr_names = ["first_name", "last_name", "dob", "phone"]

        for value, attr_name in zip(values, attr_names):
            if value is not None:
                setattr(self, attr_name, value)
        self.save()


class Profile(TimeStampedModel):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name="profile"
    )
    avatar = models.URLField(default="", max_length=2000)
    gender = models.CharField(
        choices=enums.Gender.choices, max_length=20, default=enums.Gender.Other
    )
    country = CountryField(null=False, default="VN", blank=True)
    city = models.CharField(max_length=200, default="Ho Chi Minh", blank=True)
    _nickname = models.CharField(max_length=100, null=True, unique=True)

    class Meta:
        db_table = "profile"

    @property
    def nickname(self):
        return self._nickname

    @nickname.getter
    def nickname(self):
        if not self._nickname:
            return self.user.username
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        self._nickname = value

    # Factories

    # Mutators
    def update_field(self, *, city, nickname, gender, avatar):
        """
        update only not None kwargs
        """
        values = [city, nickname, gender, avatar]
        attr_names = ["city", "nickname", "gender", "avatar"]

        for value, attr_name in zip(values, attr_names):
            if value is not None:
                setattr(self, attr_name, value)
        self.save()
