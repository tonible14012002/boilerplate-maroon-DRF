from rest_framework.permissions import BasePermission


class IsStoryOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        story = obj
        return bool(
            request.user and
            request.user.is_authenticated and
            story.user == request.user
        )
