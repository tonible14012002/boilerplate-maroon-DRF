from django.conf import settings
from django.db import models
from . import managers
from mixin.models import TimeStampedModel

# Create your models here.


class House(TimeStampedModel):
    name = models.CharField(max_length=200, null=False, blank=True)
    description = models.TextField(null=False, blank=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="houses"
    )
    address = models.CharField(max_length=200, null=False, blank=True)
    objects = managers.HouseManager()

    class Meta:
        db_table = "house"

    # ----- Queries -----
    @classmethod
    def get_joined_house(cls, user_id):
        return cls.objects.filter_by_member_id(user_id)

    # ----- Property -----
    def is_user_member(self, user):
        return self.members.filter(pk=user.pk).exists()

    def is_user_owner(self, user):
        from core_apps.permission.enums import HOUSE_PERMISSIONS

        return self.is_user_has_permissions(user, *HOUSE_PERMISSIONS)

    def is_user_has_permissions(self, user, *permission_type_names):
        from core_apps.permission.models import Permission

        return Permission.has_house_permissions(
            user, self, *permission_type_names
        )

    # ----- Factory -----
    @classmethod
    def create_new(cls, members, name, description, address):
        house = cls.objects.create(
            name=name, description=description, address=address
        )
        house.members.set(members)
        return house

    # ----- Mutator -----
    def update(self, name, description, address):
        values = [name, description, address]
        attr_names = ["name", "description", "address"]

        for value, attr_name in zip(values, attr_names):
            if value is not None:  # NOTE empty string is still allow
                setattr(self, attr_name, value)
        self.save()
        return self


class Room(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=False, blank=True)
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="rooms"
    )
    objects = managers.RoomBasicManager()

    class Meta:
        db_table = "room"

    # ----- Property -----
    def get_room_members(self):
        from core_apps.permission.models import Permission

        return Permission.get_room_assigned_users(self.id)

    def is_allow_access(self, user):
        from core_apps.permission.enums import PermissionTypeChoices

        return self.is_user_has_permissions(
            user, PermissionTypeChoices.ACCESS_ROOM
        )

    def is_allow_remove(self, user):
        from core_apps.permission.enums import PermissionTypeChoices

        return self.is_user_has_permissions(
            user, PermissionTypeChoices.DELETE_ROOM
        )

    def is_allow_update(self, user):
        from core_apps.permission.enums import PermissionTypeChoices

        return self.is_user_has_permissions(
            user, PermissionTypeChoices.ASSIGN_MEMBER
        )

    def is_allow_assign_member(self, user):
        return self.is_allow_update(user)

    def is_user_has_permissions(self, user, *permission_type_names):
        from core_apps.permission.models import Permission

        return Permission.has_room_permissions(
            user, self, *permission_type_names
        )

    # ----- Factory -----
    @classmethod
    def create_new(cls, house, name, description):
        return cls.objects.create(
            house=house, name=name, description=description
        )

    # -------------------------
    # ------- Queries ---------
    # -------------------------
    # ----- Mutator -----
    def update(self, name, description):
        values = [name, description]
        attr_names = ["name", "description"]

        for value, attr_name in zip(values, attr_names):
            if value is not None:  # NOTE empty string is still allow
                setattr(self, attr_name, value)

        self.save()
        return self
