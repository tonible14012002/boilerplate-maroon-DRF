from django.urls import path, include
from rest_framework import routers
from . import views

device_router = routers.DefaultRouter()
device_router.register(r'devices', views.DeviceViewset, basename='device')

urlpatterns = [
    path('', include(device_router.urls))
]
