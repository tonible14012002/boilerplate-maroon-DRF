from rest_framework.viewsets import (
    ModelViewSet,
    ViewSet
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from . import models
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
        return models.UserStory.objects.filter(user=user)

    def get_serializer_context(self):
        return super().get_serializer_context()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)


class FollowingStory(ViewSet, ListAPIView, RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RFollowingStory

    def get_queryset(self):
        user = self.request.user
        return models.UserStory.get_following_only(user)


class Story(ViewSet, ListAPIView):
    # NOTE: For testing only
    queryset = models.UserStory.is_active.all()
    serializer_class = serializers.RFollowingStory
