from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from . import serializers
from . import models

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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CRUDevice

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return models.Device.get_room_devices(room_id=room_id)

    def get_object(self):
        print(self.kwargs, flush=True)
        return models.Device.objects.get(id=self.kwargs["id"])

    def get_serializer(self, *args, **kwargs):
        if self.request.method not in permissions.SAFE_METHODS:
            data = kwargs.pop("data", {})
            data.setdefault("room_id", self.kwargs["room_id"])
            kwargs["data"] = data
        return super().get_serializer(*args, **kwargs)


class DeviceSpecViewset(
    viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView
):
    # Create device by RoomID
    # Update device by RoomId
    # Get devices given roomID
    lookup_field = "id"
    serializer_class = serializers.RDeiviceSpecDetail

    def get_queryset(self):
        return models.DeviceSpec.objects.all()
