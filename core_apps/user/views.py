from django.contrib.auth import get_user_model
from rest_framework import filters, views
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet
from schema import paginators

from . import serializers
from .permissions import IsAccountOwner

User = get_user_model()


# Create your views here.
class UserProfileViewset(ViewSet, RetrieveAPIView, UpdateAPIView, ListAPIView):
    """screens
    - Profile
    - Search User
    """

    queryset = User.objects.all()
    serializer_class = serializers.ReadUpdateUserProfile
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAccountOwner()]


class DeleteUserProfile(views.APIView):
    def delete(self, request, *args, **kwargs):
        request.user.profile.detele()
        request.user.delete()
        return Response(True)


class UserProfileSearch(ListAPIView):
    serializer_class = serializers.ReadUpdateUserProfile
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "last_name", "first_name", "email", "phone"]
    pagination_class = paginators.SmallSizePagination

    def get_queryset(self):
        users = User.objects.order_by_join_day()
        gender = self.request.query_params.get("gender")
        if gender:
            users = users.filter(profile__gender=gender)
        return users


class UserProfileByIds(GenericAPIView):
    """
    method: POST
    body: {
        user_ids: [...],
        detail: true
    }
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        detail = self.request.data.get("detail", None)
        if detail is not None and detail:
            return serializers.ReadUpdateUserProfile
        return serializers.ReadBasicUserProfile

    def get_queryset(self):
        user_ids = self.request.data.get("user_ids")
        return User.objects.filter(id__in=user_ids)

    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
