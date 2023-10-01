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
    followers = models.ManyToManyField("self", related_name='followings', symmetrical=False)

    REQUIRED_FIELDS = ["email", "last_name", "first_name"]

    def follow_user(self, user):
        self.followings.add(user)

    def unfollow_user(self, user):
        self.followings.remove(user)

    def check_is_follow(self, user):
        return self.followers.filter(pkid=user.pkid).exists()
