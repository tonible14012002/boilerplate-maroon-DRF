from rest_framework.viewsets import ViewSet
from rest_framework.generics import (
    RetrieveAPIView,
    UpdateAPIView,
    ListAPIView,
    CreateAPIView,
    GenericAPIView
)
from . import serializers
from .models import Profile
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)
from django.shortcuts import get_object_or_404
from core_apps.schema import paginators
from rest_framework.permissions import SAFE_METHODS
from .permissions import IsAccountOwner

User = get_user_model()


# Create your views here.
class ProfileViewSet(ViewSet, ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ReadBasicUserProfile


class UserProfileViewset(ViewSet, RetrieveAPIView, UpdateAPIView, ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ReadUpdateUserProfile
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAccountOwner()]


class ProfileRegistration(CreateAPIView):
    serializer_class = serializers.RegisterUser


class FollowUser(GenericAPIView):
    queryset = User.objects.all()
    lookup_url_kwarg = 'uid'
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        to_follow_user = self.get_object()
        user.follow_user(to_follow_user)
        return Response({'success': True}, status=HTTP_200_OK)


class UnFollowUser(FollowUser):
    def post(self, request, *args, **kwargs):
        user = request.user
        unfollow_user = self.get_object()
        user.unfollow_user(unfollow_user)
        return Response({'success': True})


class UserFollowers(ListAPIView):
    pagination_class = paginators.SmallSizePagination
    serializer_class = serializers.ReadBasicUserProfile
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        view_user = get_object_or_404(User, id=self.kwargs.get('uid', ''))
        users = view_user.followers.all()
        return users


class UserFollowings(ListAPIView):
    pagination_class = paginators.SmallSizePagination
    serializer_class = serializers.ReadBasicUserProfile

    def get_queryset(self):
        view_user = get_object_or_404(User, id=self.kwargs.get('uid', ''))
        users = view_user.followings.all()
        return users
