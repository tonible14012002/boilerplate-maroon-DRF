from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from . import models
from . import permissions as house_permissions
from . import serializers


class HouseViewset(
    viewsets.ViewSet,
    generics.CreateAPIView,
    generics.RetrieveAPIView,
    generics.ListAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
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


class RoomViewset(
    viewsets.ViewSet,
    generics.CreateAPIView,
    generics.UpdateAPIView,
    generics.RetrieveAPIView,
    generics.DestroyAPIView,
    generics.ListAPIView,
):
    lookup_field = "id"  # NOTE: use `id` instead of default primary key
    serializer_class = serializers.CRURoomDetail
    queryset = models.Room.objects.all()

    def get_queryset(self):
        house_id = self.kwargs["house_id"]
        return models.Room.objects.from_house_id(house_id)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [
            permissions.IsAuthenticated(),
            house_permissions.IsRoomHouseOwner(),
        ]

    def get_serializer(self, *args, **kwargs):
        """
        include `house_id` in data input for serialzier
        """
        if self.request.method not in permissions.SAFE_METHODS:
            data = kwargs.pop("data", {})
            data.setdefault("house_id", self.kwargs["house_id"])
            kwargs["data"] = data
        return super().get_serializer(*args, **kwargs)


class RoomAll(generics.ListAPIView):
    serializer_class = serializers.CRURoomDetail
    queryset = models.Room.objects.all()
    permission_classes = [permissions.IsAuthenticated]
