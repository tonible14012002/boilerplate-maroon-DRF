from django.shortcuts import get_object_or_404
from rest_framework import generics
from core_apps.house import models as house_models
from schema.paginators import SmallSizePagination
from . import models as notification_models
from . import serializers as notification_serializers


# Create your views here.
class RoomNotification(generics.ListAPIView):
    serializer_class = notification_serializers.RNotification

    def get_queryset(self):
        room_id = self.kwargs.get("room_id")
        room = get_object_or_404(house_models.Room, id=room_id)
        return notification_models.Notification.get_room_notifications(
            room=room
        )


class HouseNotification(generics.ListAPIView):
    serializer_class = notification_serializers.RNotification
    pagination_class = SmallSizePagination

    def get_queryset(self):
        house_id = self.kwargs.get("house_id")
        house = get_object_or_404(house_models.House, id=house_id)
        return notification_models.Notification.get_house_notifications(
            house=house,
        )


class UserNotification(generics.ListAPIView):
    serializer_class = notification_serializers.RNotification
    pagination_class = SmallSizePagination

    def get_queryset(self):
        return notification_models.Notification.get_user_notifications(
            user=self.request.user
        )
