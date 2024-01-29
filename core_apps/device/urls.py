from django.urls import path, include
from rest_framework import routers
from . import views

device_router = routers.DefaultRouter()
device_router.register(r"devices", views.DeviceViewset, basename="device")

device_spec_router = routers.DefaultRouter()
device_spec_router.register(
    "specifications", views.DeviceSpecViewset, basename="specification"
)

urlpatterns = [
    path("", include(device_router.urls)),
    path("", include(device_spec_router.urls)),
]
