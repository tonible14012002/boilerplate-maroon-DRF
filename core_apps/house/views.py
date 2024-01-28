from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from . import models

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
    serializer_class = serializers.CRUHouseDetail
    queryset = models.House.objects.all()
    permission_classes = [permissions.IsAuthenticated]
