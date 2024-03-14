from django.db import models
from mixin.models import TimeStampedModel
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from core_apps.house import models as house_models
from . import enums as notification_enums, managers as notification_managers


# Create your models here.
class Notification(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
    )
    house = models.ForeignKey(
        house_models.House,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
    )
    room = models.ForeignKey(
        house_models.Room,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
    )
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    event_code = models.CharField(
        choices=notification_enums.EventCodeChoices.choices, max_length=255
    )
    meta = models.JSONField(null=True, blank=False, encoder=DjangoJSONEncoder)

    objects = notification_managers.NotificationManager()

    class Meta:
        db_table = "notification"
        ordering = ["-created_at"]

    # --------- Factory Methods ---------
    @classmethod
    def _create_house_notification(
        cls, event_code, house, label, description, meta: dict = None
    ):
        return cls.objects.create(
            house=house,
            event_code=event_code,
            label=label,
            description=description,
            meta=meta,
        )

    @classmethod
    def create_add_house_member_notification(cls, house, invitor, new_members):
        from core_apps.user.serializers import ReadBasicUserProfile

        notification = cls._create_house_notification(
            house=house,
            event_code=notification_enums.EventCodeChoices.ADD_MEMBER_TO_HOUSE,
            label="New member joined",
            description="",
            meta={
                "invitor": ReadBasicUserProfile(invitor).data,
                "description": f"{invitor.username} has joined the house",
                "member": ReadBasicUserProfile(new_members, many=True).data,
            },
        )
        return notification

    @classmethod
    def create_update_house_metadata_notification(
        cls,
        house,
        updator,
        update_field_names,
        old_values,
    ):
        assert len(update_field_names) == len(old_values)
        from core_apps.user.serializers import ReadBasicUserProfile
        from core_apps.house.serializers import RHouseBasic

        notification = cls.create_house_notification(
            house=house,
            event_code=notification_enums.EventCodeChoices.UPDATE_HOUSE_METADATA,
            label="House info updated",
            description="",
            meta={
                "updator": ReadBasicUserProfile(updator).data,
                "house": RHouseBasic(house).data,
                "update_fields": update_field_names,
                "old_values": old_values,
            },
        )
        return notification

    @classmethod
    def _create_room_notification(
        cls, event_code, room, label, description, meta: dict = None
    ):
        return cls.objects.create(
            room=room,
            event_code=event_code,
            label=label,
            description=description,
            meta=meta,
        )

    @classmethod
    def create_add_room_member_notification(cls, room, invitor, new_members):
        from core_apps.user.serializers import ReadBasicUserProfile
        from . import enums

        notification = cls._create_room_notification(
            room=room,
            event_code=enums.EventCodeChoices.INVITE_MEMBER_TO_ROOM,
            label="Add members to room",
            description="",
            meta={
                "invitor": ReadBasicUserProfile(invitor).data,
                "description": f"{invitor.username} invited new members to room {room.name}",
                "new_members": ReadBasicUserProfile(
                    new_members, many=True
                ).data,
            },
        )
        return notification

    # --------- Queries ---------
    @classmethod
    def get_house_notifications(cls, house):
        return cls.objects.filter(
            house=house,
            event_code__in=notification_enums.HOUSE_NOTIFICATION_EVENT_CODES,
        ).order_by("-created_at")

    @classmethod
    def get_room_notifications(cls, room):
        return cls.objects.filter(
            room=room,
            event_code__in=notification_enums.ROOM_NOTIFICATION_EVENT_CODES,
        ).order_by("-created_at")

    @classmethod
    def get_user_notifications(cls, user):
        return cls.objects.filter(user=user).order_by("-created_at")
