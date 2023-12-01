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
from rest_framework import exceptions
from core_apps.common.utils import db as common_db_utils
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


class FollowingStoryViewset(ViewSet, ListAPIView, RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RFollowingStory

    def get_story_inbox_query(self, user_pkid):
        return '''
            SELECT story_id FROM db.story_inbox
            WHERE user_id = '{user_id}'
            ALLOW FILTERING;
        '''.format(user_id=user_pkid)

    def get_queryset(self):
        user = self.request.user
        try:
            connection = common_db_utils.cassandra_connection()
            query = self.get_story_inbox_query(user.pkid)
            print(query, flush=True)
            with connection.cursor() as cursor:
                story_ids = map(lambda id_dic: id_dic['story_id'], cursor.execute(
                    query
                ))
        except Exception as e:
            print(e, flush=True)
            raise exceptions.NotFound()

        return models.UserStory.from_pkids(story_ids)


class Story(ViewSet, ListAPIView):
    # NOTE: For testing only
    queryset = models.UserStory.is_active.all()
    serializer_class = serializers.RFollowingStory


class PostStory(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CRUStoryDetail

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            story = serializer.save()

            # Schedule Task For Push to Cassandra StoryInbox
            task.boardcast_story_inbox.delay(
                request.user.pkid,
                story.pkid,
                story.live_time
            )

            return response.Response(
                serializers.CRUStoryDetail(story).data,
                status=status.HTTP_200_OK
            )
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
