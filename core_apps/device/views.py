from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from .import serializers
from . import models
# Create your views here.

Device = models.Device


class DeviceViewset(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView):
    queryset = models.Device.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.DeviceSerializer
