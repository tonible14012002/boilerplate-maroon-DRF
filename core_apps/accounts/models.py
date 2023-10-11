from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core_apps.common.models import TimeStampedModel
from django_countries.fields import CountryField
from core_apps.common.models.mixins import UpdateModelFieldMixin
from django.contrib.auth.hashers import make_password
from . import enums
from . import managers
import uuid


# Create your models here.
class MyUser(AbstractUser):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    dob = models.DateField(null=True)
    phone = PhoneNumberField()
    followers = models.ManyToManyField("self", related_name='followings', symmetrical=False)
    objects = managers.UserManager()

    REQUIRED_FIELDS = ["email", "last_name", "first_name"]

    # Factory
    @classmethod
    def create_register(cls, *, username: str, password: str, extra_fields: dict, profile_fields: dict):
        # NOTE: Use this method for create new user instead of objects.create()
        user = cls.objects.create(
            username=username,
            password=make_password(password),
            **extra_fields
        )
        Profile.objects.create(
            user=user,
            **profile_fields
        )
        return user

    # Properties
    @property
    def is_following_user(self, user):
        return self.followers.filter(pkid=user.pkid).exists()

    @property
    def is_following_user_pk(self, userPk):
        return self.followers.filter(pkid=userPk).exists()

    @property
    def total_followers(self):
        return self.followers.count()

    @property
    def total_followings(self):
        return self.followings.count()

    # Mutators
    def update_field(self, *, first_name, last_name, dob, phone):
        values = [first_name, last_name, dob, phone]
        attr_names = ['first_name', 'last_name', 'dob', 'phone']

        for value, attr_name in zip(values, attr_names):
            if value is not None:
                setattr(self, attr_name, value)
        self.save()

    def update_followers(self, users: list):
        self.followers.set(users)

    def unfollow_user(self, *user):
        self.followings.remove(*user)

    def follow_user(self, *user,):
        self.followings.add(*user)


class Profile(TimeStampedModel, UpdateModelFieldMixin):

    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(default='', max_length=2000)
    gender = models.CharField(choices=enums.Gender.choices, max_length=20, default=enums.Gender.Other)
    country = CountryField(null=False, default="VN")
    city = models.CharField(max_length=200, default="Ho Chi Minh")
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
        '''
        update only not None kwargs
        '''
        values = [city, nickname, gender, avatar]
        attr_names = ['city', 'nickname', 'gender', 'avatar']

        for value, attr_name in zip(values, attr_names):
            if value is not None:
                setattr(self, attr_name, value)
        self.save()
