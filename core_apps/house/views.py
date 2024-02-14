from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import filters
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from core_apps.user import serializers as user_serializers
from schema import paginators
from . import models
from . import permissions as house_permissions
from . import serializers

User = get_user_model()


class HouseViewset(
    viewsets.ViewSet,
    generics.CreateAPIView,
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
    generics.ListAPIView,
):
    lookup_field = "id"
    queryset = models.House.objects.all()
    serializer_class = serializers.CRUHouseDetail

    def get_permissions(self):
        # For testing only, get all houses in system
        if self.action == "list":
            return [
                permissions.IsAuthenticated(),
            ]
        if self.action == "create":
            return [
                permissions.IsAuthenticated(),
            ]
        if self.action == "retrieve":
            return [
                permissions.IsAuthenticated(),
                house_permissions.IsHouseMember(),
            ]
        if self.action == "update" or self.action == "partial_update":
            return [
                permissions.IsAuthenticated(),
                house_permissions.IsHouseOwner(),
            ]
        if self.action == "destroy":
            return [
                permissions.IsAuthenticated(),
                house_permissions.IsHouseOwner(),
            ]
        return []


class HouseJoined(generics.ListAPIView):
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CRUHouseDetail

    def get_queryset(self):
        return models.House.get_joined_house(self.request.user.id)


class RoomListCreateViewset(
    viewsets.ViewSet,
    generics.CreateAPIView,
    generics.ListAPIView,
):
    lookup_field = "id"  # NOTE: use `id` instead of default primary key
    serializer_class = serializers.CRURoomDetail

    def get_queryset(self):
        house_id = self.kwargs["house_id"]
        return models.Room.objects.from_house_id(house_id)

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAuthenticated()]
        if self.action == "create":
            return [
                permissions.IsAuthenticated(),
                house_permissions.IsHouseOwner(),
            ]
        if self.action == "retrieve":
            return [
                permissions.IsAuthenticated(),
                house_permissions.IsRoomAcessible(),
            ]
        return [
            permissions.IsAuthenticated(),
            house_permissions.IsRoomRemovable(),
        ]

    def get_serializer(self, *args, **kwargs):
        # include `house_id` in data input for serialzier
        if self.request.method not in permissions.SAFE_METHODS:
            data = kwargs.pop("data", {})
            data.setdefault("house_id", self.kwargs["house_id"])
            kwargs["data"] = data
        return super().get_serializer(*args, **kwargs)


class RoomRetrieveUpdateViewset(
    viewsets.ViewSet,
    generics.UpdateAPIView,
    generics.RetrieveAPIView,
    generics.DestroyAPIView,
):
    lookup_field = "id"  # NOTE: use `id` instead of default primary key
    serializer_class = serializers.CRURoomDetail
    queryset = models.Room.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == "update":
            data = kwargs.pop("data", {})
            data.setdefault("house_id", self.get_object().house_id)
            kwargs["data"] = data
        return super().get_serializer(*args, **kwargs)

    def get_permissions(self):
        if self.action == "update":
            return [
                permissions.IsAuthenticated(),
                house_permissions.IsRoomAdmin(),
            ]
        if self.action == "retrieve":
            return [
                permissions.IsAuthenticated(),
                house_permissions.IsRoomAcessible(),
            ]
        return [
            permissions.IsAuthenticated(),
            house_permissions.IsRoomRemovable(),
        ]


class RoomAll(generics.ListAPIView):
    serializer_class = serializers.CRURoomDetail
    queryset = models.Room.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class RemoveHouseMember(APIView):
    """
    Allow remove non-owner members from house
    """

    permission_classes = [
        permissions.IsAuthenticated,
        house_permissions.IsAllowRemoveHouse,
    ]

    def post(self, request, house_id):
        from core_apps.permission.models import Permission
        from core_apps.permission.enums import HOUSE_PERMISSIONS

        data = request.data
        serializer = serializers.RemoveHouseMember(data=data)
        if serializer.is_valid(raise_exception=True):
            to_remove_ids = serializer.validated_data["remove_members"]
            house = models.House.objects.get(id=house_id)
            # VALIDATE PREVENT REMOVE HOUSE's OWNER
            if self.has_owner_ids(to_remove_ids, house=house):
                return response.Response(
                    {"error": "Cannot remove owner from house"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # REMOVE MEMBERS AND THEIR PERMISSIONS
            house.members.remove(*User.objects.filter(id__in=to_remove_ids))
            Permission.objects.filter(
                permission_type__name__in=HOUSE_PERMISSIONS, houses=house
            ).delete()
            return response.Response(status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_400_BAD_REQUEST)

    def has_owner_ids(self, to_remove_ids, house):
        from core_apps.permission.enums import HOUSE_PERMISSIONS

        return (
            User.objects.filter(
                permissions__houses=house,
                id__in=to_remove_ids,
            )
            .annotate(permission_count=Count("permissions__id"))
            .filter(permission_count=len(HOUSE_PERMISSIONS))
            .exists()
        )


class AddHouseMember(generics.CreateAPIView):
    lookup_field = "house_id"
    queryset = models.House.objects.all()
    serializer_class = serializers.AddHouseMember
    permission_classes = [
        permissions.IsAuthenticated,
        house_permissions.IsAllowInviteHouseMember,
    ]

    def get_serializer(self, *args, **kwargs):
        kwargs["data"].setdefault("house_id", self.kwargs["house_id"])
        return super().get_serializer(*args, **kwargs)


class RoomMember(generics.ListAPIView):
    serializer_class = serializers.RoomMember

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        room = models.Room.objects.get(id=room_id)
        return room.get_room_members()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["room_id"] = self.kwargs["room_id"]
        return context


class NonRoomMemberUserProfileSearch(generics.ListAPIView):
    """
    Filter User in current house whoses does not have some permission to a room
    params: `exclude_permissions` (optional) - comma separated list of permission
    """

    serializer_class = user_serializers.ReadBasicUserProfile
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "last_name", "first_name", "email", "phone"]
    pagination_class = paginators.SmallSizePagination

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        exclude_permissions = self.request.query_params.get(
            "exclude_permissions", ""
        ).split(",")

        room = models.Room.objects.select_related("house").get(id=room_id)
        house = room.house
        return house.members.exclude(
            permissions__rooms=room,
            permissions__permission_type__name__in=exclude_permissions,
        )


class RoomPermissionAll(APIView):
    def get(self, request):
        from core_apps.permission.enums import ROOM_PERMISSIONS

        return response.Response(
            {"permissions": ROOM_PERMISSIONS},
            status=status.HTTP_200_OK,
        )


class HousePermissionAll(APIView):
    def get(self, request):
        from core_apps.permission.enums import HOUSE_PERMISSIONS

        return response.Response(
            {"permissions": HOUSE_PERMISSIONS},
            status=status.HTTP_200_OK,
        )


class NonHouseMemberUserProfileSearch(generics.ListAPIView):
    serializer_class = user_serializers.ReadBasicUserProfile
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "last_name", "first_name", "email", "phone"]
    pagination_class = paginators.SmallSizePagination

    def get_queryset(self):
        house_id = self.kwargs["house_id"]
        users = User.objects.exclude(houses__id=house_id).order_by_join_day()
        gender = self.request.query_params.get("gender")
        if gender:
            users = users.filter(profile__gender=gender)
        return users


class HouseMember(generics.ListAPIView):
    serializer_class = serializers.HouseMember
    permission_classes = [
        permissions.IsAuthenticated,
        house_permissions.IsHouseMember,
    ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["house_id"] = self.kwargs["house_id"]
        return context

    def get_queryset(self):
        house_id = self.kwargs["house_id"]
        house = get_object_or_404(models.House, id=house_id)
        return house.members.all()


class UpdateHouseMemberPermissions(generics.UpdateAPIView):
    serializer_class = serializers.UHouseMember

    permission_classes = [
        permissions.IsAuthenticated,
        house_permissions.IsUserHouseOwner,
    ]

    def get_object(self):
        user_id = self.kwargs["member_id"]
        return get_object_or_404(User, id=user_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["house_id"] = self.kwargs["house_id"]
        return context


class UpdateRoomMemberPermissions(generics.UpdateAPIView):
    serializer_class = serializers.URoomMember

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        user_id = self.kwargs["member_id"]
        return get_object_or_404(User, id=user_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["room_id"] = self.kwargs["room_id"]
        return context
