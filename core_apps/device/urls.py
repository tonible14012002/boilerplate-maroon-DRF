from django.urls import path, include
from rest_framework import routers
from . import views

device_router = routers.DefaultRouter()
device_router.register("", views.RoomDeviceViewset, basename="device")

device_spec_router = routers.DefaultRouter()
device_spec_router.register(
    "", views.DeviceSpecViewset, basename="specification"
)

urlpatterns = [
    path("room/<uuid:room_id>/devices/", include(device_router.urls)),
    path(
        "devices/<uuid:id>/",
        views.RetrieveDeviceDetailView.as_view(),
    ),
    path("specifications/", include(device_spec_router.urls)),
]
