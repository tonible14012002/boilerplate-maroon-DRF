from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class ExpiredStoryManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(expire_date__lt=timezone.now())


class ActiveStoryManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(expire_date__gt=timezone.now())

    def following_only(self, user) -> QuerySet:
        return self.get_queryset().filter(
            user__followings=user,
        )
