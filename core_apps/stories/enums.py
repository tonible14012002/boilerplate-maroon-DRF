from django.db import models


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


class LiveTime(models.IntegerChoices):
    HalfDay = 4300
    OneDay = 8600
    TwoDay = 17200


class ViewOption(models.TextChoices):
    OnlyMe = ('ONLY_ME', 'Only me')
    Everyone = ('EVERYONE', 'Every one')
