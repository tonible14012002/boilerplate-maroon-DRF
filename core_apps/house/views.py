from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import response
from rest_framework.views import APIView
from rest_framework import status
from core_apps.user import serializers as user_serializers
from . import models
from . import permissions as house_permissions
from . import serializers


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
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [
            permissions.IsAuthenticated(),
            house_permissions.IsHouseOwner(),
        ]


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


class RemoveHouseMember(generics.ListAPIView):
    pass


class AddHouseMember(generics.UpdateAPIView):
    pass


class RoomMember(generics.ListAPIView):
    serializer_class = user_serializers.ReadBasicUserProfile

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        room = models.Room.objects.get(id=room_id)
        return room.get_room_members()


class HouseMemberWithoutRoomPermission(generics.ListAPIView):
    """
    Filter User in current house whoses does not have some permission to a room
    params: `exclude_permissions` (optional) - comma separated list of permission
    """

    serializer_class = user_serializers.ReadBasicUserProfile

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        exclude_permissions = self.request.query_params.get(
            "exclude_permissions"
        )

        room = models.Room.objects.select_related("house").get(id=room_id)
        house = room.house
        return house.members.exclude(
            permissions__rooms=room,
            permissions__permission_type__name__in=exclude_permissions,
        )


# class AssignRoomMember(generics.UpdateAPIView):
#     lookup_field = "id"
#     queryset = models.Room.objects.all()
#     permission_classes = [
#         permissions.IsAuthenticated,
#         house_permissions.IsRoomAdmin,
#     ]
#     serializer_class = serializers.URoomMember


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
