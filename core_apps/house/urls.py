from django.urls import path, include
from rest_framework import routers
from . import views

house_router = routers.DefaultRouter()
house_router.register("", views.HouseViewset, "houses")

room_router = routers.DefaultRouter()
room_router.register("", views.RoomViewset, "rooms")

urlpatterns = [
    path("houses/rooms/", views.RoomAll.as_view()),
    path("houses/<uuid:house_id>/rooms/", include(room_router.urls)),
    path("houses/", include(house_router.urls)),
]
