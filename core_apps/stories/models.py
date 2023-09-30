from django.db import models
from django.conf import settings
from core_apps.common.models import TimeStampedModel
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class UserStory(TimeStampedModel):
    class StoryStatus(models.TextChoices):
        New = ('NEW', 'New')
        Expired = ('EXPIRED', 'Expired')

    class PrivacyMode(models.TextChoices):
        Private = ('PRIVATE', 'Private')
        Public = ('PUBLIC', 'Public')
        FriendOnly = ('FRIEND_ONLY', 'Friend only')

    class MediaType(models.TextChoices):
        Video = ('VIDEO', 'Video')
        Image = ('IMAGE', 'Image')

    class MediaDuration(models.IntegerChoices):
        Min = 5,
        Medium = 10,
        Long = 15
        ExtraLong = 30

    class LiveTimeOption(models.IntegerChoices):
        HalfDay = 4300
        OneDay = 8600
        TwoDay = 17200

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
        choices=LiveTimeOption.choices,
        default=LiveTimeOption.OneDay
    )
    expire_date = models.DateTimeField(null=True)
    status = models.CharField(
        choices=StoryStatus.choices,
        default=StoryStatus.New,
        max_length=50
    )
    duration = models.PositiveSmallIntegerField(
        choices=MediaDuration.choices,
        default=MediaDuration.Medium
    )
    media_type = models.CharField(
        choices=MediaType.choices,
        default=MediaType.Video,
        max_length=20
    )
    privacy_mode = models.CharField(
        choices=PrivacyMode.choices,
        default=PrivacyMode.FriendOnly,
        max_length=20
    )

    class Meta:
        db_table = 'story'

    def exclude_user(self, user):
        self.excluded_users.add(user)

    def allow_user(self, user):
        self.excluded_users.remove(user)

    def all_views(self):
        return self.story_views.all()

    def is_viewed_by(self, user):
        return self.story_views.filter(user=user).exist()

    def save(self, *args, **kwargs):
        if not (self.id and self.expire_date):
            livetime = self.live_time if self.live_time else self.LiveTimeOption.OneDay
            self.expire_date = timezone.now() + timedelta(seconds=livetime)
        return super(UserStory, self).save(*args, **kwargs)


class StoryView(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='story_views')
    story = models.ForeignKey(UserStory, on_delete=models.CASCADE, related_name='story_views')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'story_viewer'
        unique_together = ['user', 'story']
