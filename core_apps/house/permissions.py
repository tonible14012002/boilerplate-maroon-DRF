from rest_framework import permissions


class IsHouseOwner(permissions.BasePermission):
    """
    required `IsAuthenticated` permission
    """

    def has_object_permission(self, request, view, obj):
        house = obj
        return (
            request.user
            and request.user.is_authenticated
            and house.is_user_owner(request.user)
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
            and room.house.is_user_owner(request.user)
        )
