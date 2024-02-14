from rest_framework import permissions
from core_apps.permission.enums import PermissionTypeChoices


class IsHouseMember(permissions.BasePermission):
    """
    required `IsAuthenticated` permission
    """

    def has_object_permission(self, request, view, obj):
        house = obj
        return (
            request.user
            and request.user.is_authenticated
            and house.is_user_member(request.user)
        )


class IsHouseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        house = obj
        return (
            request.user
            and request.user.is_authenticated
            and house.is_user_owner(request.user)
        )


class IsUserHouseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        from . import models

        house_id = view.kwargs.get("house_id")
        house = models.House.objects.get(id=house_id)
        return house.is_user_owner(request.user)


class IsRoomHouseOwner(permissions.BasePermission):
    """
    required `IsAuthenticated` permission
    """

    def has_object_permission(self, request, view, obj):
        room = obj
        return (
            request.user
            and request.user.is_authenticated
            and room.house.is_user_member(request.user)
        )


class IsRoomAcessible(permissions.BasePermission):
    """
    required `IsAuthenticated` permission
    """

    def has_object_permission(self, request, view, obj):
        room = obj
        return room.is_allow_access(request.user)


class IsRoomRemovable(permissions.BasePermission):
    """
    required `IsAuthenticated` permission
    """

    def has_object_permission(self, request, view, obj):
        room = obj
        return room.is_allow_remove(request.user)


class IsRoomAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        room = obj
        return room.is_allow_update(request.user)


class BaseHasHousePermission(permissions.BasePermission):
    """
    Base genericAPI Permission Class for checking house permission
    """

    permission_type_names = None

    def get_permission_type(self):
        assert self.permission_type_names is not None, (
            "'%s' should include a `permission_type_names` attribute, "
            "or override the `get_permission_type()` method."
            % self.__class__.__name__
        )
        if not isinstance(self.permission_type_names, list):
            self.permission_type_names = []
        return self.permission_type_names

    def has_object_permission(self, request, view, obj):
        house = obj
        return house.is_user_has_permissions(
            request.user, *self.get_permission_type()
        )


class IsAllowInviteHouseMember(BaseHasHousePermission):
    permission_type_names = [PermissionTypeChoices.INVITE_HOUSE_MEMBER]


class IsAllowRemoveHouseMember(BaseHasHousePermission):
    permission_type_names = [PermissionTypeChoices.REMOVE_HOUSE_MEMBER]


class IsAllowRemoveHouse(BaseHasHousePermission):
    permission_type_names = [PermissionTypeChoices.REMOVE_HOUSE]
