from django.db import models
from django.conf import settings
from core_apps.common.models import TimeStampedModel


# Create your models here.
class UserStory(TimeStampedModel):
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

    media_url = models.URLField()
    live_time = models.PositiveSmallIntegerField(
        default=settings.APPS_CONFIG['STORIES']['default_live_time']
    )
    expired = models.BooleanField(default=False)
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

    def all_viewers(self):
        return self.story_views.all()

    def is_viewed_by(self, user):
        return self.story_views.filter(user=user).exist()


class StoryView(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='story_views')
    story = models.ForeignKey(UserStory, on_delete=models.CASCADE, related_name='story_views')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'story_viewer'
        unique_together = ['user', 'story']
