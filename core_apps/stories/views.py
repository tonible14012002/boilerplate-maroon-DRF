from rest_framework.viewsets import (
    ModelViewSet,
    ViewSet
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    GenericAPIView
)
from . import models
from . import serializers
from .permissions import (
    IsStoryOwner
)
from rest_framework import response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from . import story_inbox
from . import task


# Create your views here.
class UserAchievedStoryViewset(ModelViewSet):
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


class AllFollowingStory(ListAPIView, RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RFollowingStory

    def get_queryset(self):
        user = self.request.user
        owner_id = self.request.query_params.get('owner_id')
        inbox = story_inbox.StoryInbox(user_id=user.id)
        if owner_id:
            return inbox.get_all_from_user(sender_id=owner_id)
        else:
            return inbox.get_all()


class Story(ViewSet, ListAPIView):
    # NOTE: For testing only
    queryset = models.UserStory.is_active.all()
    serializer_class = serializers.RFollowingStory


class PostStory(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CRUStoryDetail

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            story = serializer.save()

            # Schedule Task For Push to Cassandra StoryInbox
            task.boardcast_story_inbox.delay(
                request.user.id,
                story.id,
                story.live_time
            )

            # inbox = story_inbox.StoryInbox(request.user.id)
            # inbox.send_story(story_id=story.id, ttl=story.live_time)

            return response.Response(
                serializers.CRUStoryDetail(story).data,
                status=status.HTTP_200_OK
            )

        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
