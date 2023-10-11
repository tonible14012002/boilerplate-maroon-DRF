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

    def get_friend_stories(self, user):
        friend_stories = self.get_queryset().filter(
            user__followings=user,
        )
        return friend_stories
        # stories = self.get_queryset().filter()
        # get friend list that have stories available
