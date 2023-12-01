from django.db import models
from django.conf import settings
from core_apps.common.models import TimeStampedModel
from django.utils import timezone
from datetime import timedelta
from core_apps.common.models.mixins import UpdateModelFieldMixin
from core_apps.accounts import models as account_models
from . import enums
from .managers import (
    ExpiredStoryManager,
    ActiveStoryManager
)

# Logic on single model's instance must use model method
# Logic on  set of model's instance must use manager method
# Logic on  set of model's instance with realate model's instance
# Try put all relate method of a model in manager
# To interact with other model, use model classmethod


# Create your models here.
class UserStory(TimeStampedModel, UpdateModelFieldMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name='stories'
    )

    excluded_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='excluded_stories'
    )

    media_url = models.URLField(max_length=2000)
    live_time = models.PositiveSmallIntegerField(
        choices=enums.LiveTime.choices,
        default=enums.LiveTime.OneDay
    )
    expire_date = models.DateTimeField(null=True)
    status = models.CharField(
        choices=enums.StoryStatus.choices,
        default=enums.StoryStatus.New,
        max_length=50
    )
    duration = models.PositiveSmallIntegerField(
        choices=enums.MediaDuration.choices,
        default=enums.MediaDuration.Medium
    )
    media_type = models.CharField(
        choices=enums.MediaType.choices,
        default=enums.MediaType.Video,
        max_length=20
    )
    privacy_mode = models.CharField(
        choices=enums.PrivacyMode.choices,
        default=enums.PrivacyMode.FriendOnly,
        max_length=20
    )

    objects = models.Manager()
    is_expired = ExpiredStoryManager()
    is_active = ActiveStoryManager()

    class Meta:
        db_table = 'story'
        ordering = ['-updated_at', '-created_at']

    # Factories
    @classmethod
    def create_new(cls, *, user, privacy_mode, media_url, duration, media_type, live_time):
        return cls.objects.create(
            user=user,
            expire_date=timezone.now() + timedelta(seconds=live_time),
            privacy_mode=privacy_mode,
            media_url=media_url,
            media_type=media_type,
            duration=duration
        )

    # Properties
    def is_viewed_by(self, user):
        return self.story_views.filter(user=user).exist()

    # Queries
    @classmethod
    def get_for_followers(cls):
        stories = cls.is_active.following_only()
        return stories

    # Deprecated Method
    @classmethod
    def get_following_only(cls, user):
        return cls.is_active.following_only(user)

    @classmethod
    def from_pkids(cls, pkids):
        return cls.objects.filter(pkid__in=pkids)

    # Mutator
    def exclude_user(self, user: account_models.MyUser):
        self.excluded_users.add(user)

    def allow_user(self, user):
        self.excluded_users.remove(user)

    def reset_exclude_users(self, users):
        self.excluded_users.set(users)


class StoryView(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='story_views')
    story = models.ForeignKey(UserStory, on_delete=models.CASCADE, related_name='story_views')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'story_viewer'
        unique_together = ['user', 'story']
        ordering = ['-viewed_at']
