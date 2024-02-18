from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from django.shortcuts import get_object_or_404
from schema import paginators
from . import serializers
from . import models
from . import permissions as device_permissions

# Create your views here.


class RoomDeviceViewset(
    viewsets.ViewSet,
    generics.ListAPIView,
    generics.CreateAPIView,
    generics.UpdateAPIView,
    generics.RetrieveAPIView,
    generics.DestroyAPIView,
):
    lookup_field = "id"
    serializer_class = serializers.CRUDevice
    permission_classes = [
        permissions.IsAuthenticated,
        device_permissions.HasUpdateRoomPermission,
    ]

    def get_queryset(self):
        room = self.get_room()
        return models.Device.get_room_devices(room_id=room.id)

    def get_object(self):
        return models.Device.objects.get(id=self.kwargs["id"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["room"] = self.get_room()
        return context

    def get_room(self):
        from core_apps.house import models as house_models

        if not hasattr(self, "room"):
            self.room = get_object_or_404(
                house_models.Room, id=self.kwargs["room_id"]
            )
            return self.room
        else:
            return self.room


class DeviceSpecViewset(
    viewsets.ViewSet,
    generics.ListAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    lookup_field = "id"
    serializer_class = serializers.RDeiviceSpecDetail
    filter_backends = []
    queryset = models.DeviceSpec.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
        "series_name",
        "gpu",
        "gpu_max_fre",
        "cpu",
        "cpu_max_fre",
        "vision_acceleration",
        "storage",
        "memory",
        "power",
    ]
    pagination_class = paginators.SmallSizePagination
