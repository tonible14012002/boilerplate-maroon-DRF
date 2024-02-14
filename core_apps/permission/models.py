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
    def has_house_permissions(cls, user, house, *permission_names):
        """
        check if user has all house's permission in given permission_names
        """
        return cls.objects.filter(
            user=user, permission_type__name__in=permission_names, houses=house
        ).distinct().count() == len(permission_names)

    @classmethod
    def get_user_house_permissions(cls, user, house, flat=False):
        if flat:
            return cls.objects.filter(user=user, houses=house).values_list(
                "permission_type__name", flat=True
            )
        return cls.objects.filter(user=user, houses=house)

    # -----------------------------------
    # ----- ROOM PERMISSION HANDLER -----
    # -----------------------------------
    # ----- Mutator -----
    @classmethod
    def grant_all_room_permissions(cls, user, *rooms):
        for permission_name in enums.ROOM_PERMISSIONS:
            cls.grant_rooms_permission(user, permission_name, *rooms)

    @classmethod
    def grant_rooms_permission(cls, user, permission_name, *rooms):
        permission, _ = cls.objects.get_or_create(
            user=user,
            permission_type=PermissionType.get_permission_type(
                permission_name
            ),
        )
        permission.rooms.add(*rooms)

    # ----- Queries -----
    @classmethod
    def get_room_assigned_users(cls, room_id):
        room_pers = cls.objects.select_related("user").filter(
            rooms__id=room_id,
        )
        print(room_pers, flush=True)
        return list(set(per.user for per in room_pers))

    @classmethod
    def get_user_room_permissions(cls, user, room, flat=False):
        if flat:
            return cls.objects.filter(user=user, rooms=room).values_list(
                "permission_type__name", flat=True
            )
        return cls.objects.filter(user=user, rooms=room)

    # ----- Properties

    @classmethod
    def has_room_permissions(cls, user, room, *permission_names):
        """
        check if user has all permission in given permission_names
        """
        return cls.objects.filter(
            user=user, permission_type__name__in=permission_names, rooms=room
        ).distinct().count() == len(permission_names)

    # ----- Mutator -----
