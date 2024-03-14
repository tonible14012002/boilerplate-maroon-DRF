from rest_framework import permissions


class HasUpdateRoomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.get_room().is_allow_update(request.user)
