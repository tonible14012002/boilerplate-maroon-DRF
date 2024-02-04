from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from core_apps.house.models import Room, House
from . import enums

User = get_user_model()


# Create your models here.
class PermissionType(models.Model):
    name = models.CharField(
        enums.PermissionTypeChoices.choices,
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )
    description = models.TextField(null=False, blank=True)

    class Meta:
        db_table = "permission_type"

    @classmethod
    def get_permission_type(cls, permission_name):
        return cls.objects.get(name=permission_name)


class Permission(models.Model):

    permission_type = models.ForeignKey(
        PermissionType,
        on_delete=models.CASCADE,
        related_name="permissions",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="permissions",
    )
    # House rooms that current permission is applied to
    rooms = models.ManyToManyField(Room, related_name="permissions")
    houses = models.ManyToManyField(House, related_name="permissions")
    # Add other model permission here

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_permission"
        unique_together = ("permission_type", "user")
        # Add indexing for permission, user

    # -----------------------------------
    # ----- HOUSE PERMISSION HANDLER -----
    # -----------------------------------

    @classmethod
    def grant_houses_permission(cls, user, permission_type, *houses):
        try:
            permission = cls.objects.get(
                user=user, permission_type=permission_type
            )
            permission.houses.add(*houses)
        except cls.DoesNotExist:
            permission = cls.objects.create(
                user=user,
                permission_type=permission_type,
            )
            permission.houses.set(houses)

    @classmethod
    def grant_houses_owner_permissions(cls, user, *houses):
        for permission_name in enums.HOUSE_PERMISSIONS:
            permission_type = PermissionType.get_permission_type(
                permission_name
            )
            cls.grant_houses_permission(user, permission_type, *houses)

    @classmethod
    def is_house_owner(cls, user, house):
        if not cls.objects.filter(
            user=user,
            permission_type__name__in=enums.HOUSE_PERMISSIONS,
            houses__id=house.id,
        ).exists():
            return False
        return True

    # -----------------------------------
    # ----- ROOM PERMISSION HANDLER -----
    # -----------------------------------
    @classmethod
    def grant_all_room_permissions(cls, user, *rooms):
        for permission_name in enums.ROOM_PERMISSIONS:
            permission_type = PermissionType.get_permission_type(
                permission_name
            )
            cls.grant_rooms_permission(user, permission_type, *rooms)

    @classmethod
    def grant_rooms_permission(cls, user, permission_type, *rooms):
        try:
            permission = cls.objects.get(
                user=user, permission_type=permission_type
            )
            permission.rooms.add(*rooms)
        except cls.DoesNotExist:
            permission = cls.objects.create(
                user=user,
                permission_type=permission_type,
            )
            permission.rooms.set(rooms)

    @classmethod
    def get_room_assigned_users(cls, room_id):
        room_pers = cls.objects.select_related("user").filter(
            rooms__id=room_id,
        )
        print(room_pers, flush=True)
        return list(set(per.user for per in room_pers))

    # ----- Queries -----
    # ----- Properties

    @classmethod
    def has_room_permission(cls, user, permission_type, room):
        return cls.objects.filter(
            user=user, permission_type=permission_type, rooms=room
        ).exists()

    # ----- Mutator -----
