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
class UserAchievedStoryViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsStoryOwner]
    serializer_class = serializers.CRUStoryDetail
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return UserStory.objects.filter(user=user)

    def get_serializer_context(self):
        return super().get_serializer_context()


class FriendStoryViewset(ViewSet, ListAPIView, RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RFriendStory

    def get_queryset(self):
        user = self.request.user
        return UserStory.is_active.get_friend_stories(user=user)
