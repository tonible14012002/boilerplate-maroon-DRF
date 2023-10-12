from rest_framework.viewsets import (
    ModelViewSet,
    ViewSet
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from .models import (
    UserStory,
)
from . import serializers
from .permissions import (
    IsStoryOwner
)
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserAchievedStory(ModelViewSet):
    permission_classes = [IsAuthenticated, IsStoryOwner]
    serializer_class = serializers.CRUStoryDetail
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return UserStory.objects.filter(user=user)

    def get_serializer_context(self):
        return super().get_serializer_context()


class FollowingStory(ViewSet, ListAPIView, RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RFollowingStory

    def get_queryset(self):
        user = self.request.user
        return UserStory.get_active_from_owners(user.followings.all())
