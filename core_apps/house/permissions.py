from rest_framework import permissions
from core_apps.permission import models as permission_models


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
            and permission_models.Permission.is_house_owner(
                request.user, house
            )
        )


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
