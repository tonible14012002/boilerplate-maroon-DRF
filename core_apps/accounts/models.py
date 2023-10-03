from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import UserManager
from .managers import AccountManager
from core_apps.common.models import TimeStampedModel
from django_countries.fields import CountryField
import uuid


# Create your models here.
class MyUser(AbstractUser):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    dob = models.DateField(null=True)
    phone = PhoneNumberField()
    followers = models.ManyToManyField("self", related_name='followings', symmetrical=False)
    objects = UserManager()
    manager = AccountManager()

    REQUIRED_FIELDS = ["email", "last_name", "first_name"]

    def follow_user(self, user):
        self.followings.add(user)

    def unfollow_user(self, user):
        self.followings.remove(user)

    def check_is_follow(self, user):
        return self.followers.filter(pkid=user.pkid).exists()


class Profile(TimeStampedModel):

    class GENDER(models.TextChoices):
        MALE = ('MALE', 'Male')
        FEMALE = ('FEMALE', 'Female')
        OTHER = ('OTHER', 'Other')

    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(default='', max_length=2000)
    gender = models.CharField(choices=GENDER.choices, max_length=20, default=GENDER.OTHER)
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
