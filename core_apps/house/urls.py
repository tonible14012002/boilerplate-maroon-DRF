from django.urls import path, include
from rest_framework import routers
from . import views

house_router = routers.DefaultRouter()
house_router.register("", views.HouseViewset, "houses")

room_router = routers.DefaultRouter()
room_router.register("", views.RoomListCreateViewset, "rooms")

room_detail_router = routers.DefaultRouter()
room_detail_router.register("", views.RoomRetrieveUpdateViewset, "room-detail")

urlpatterns = [
    path("houses/room-permissions/", views.RoomPermissionAll.as_view()),
    path("houses/house-permissions/", views.HousePermissionAll.as_view()),
    path("houses/joined/", views.HouseJoined.as_view()),
    path("houses/rooms/", views.RoomAll.as_view()),
    path("houses/rooms/<uuid:room_id>/members/", views.RoomMember.as_view()),
    path(
        "houses/rooms/<uuid:room_id>/add-members/search/",
        views.NonRoomMemberUserProfileSearch.as_view(),
    ),
    path("houses/<uuid:house_id>/rooms/", include(room_router.urls)),
    path("houses/room-detail/", include(room_detail_router.urls)),
    path(
        "houses/<uuid:house_id>/remove-members/",
        views.RemoveHouseMember.as_view(),
    ),
    path(
        "houses/<uuid:house_id>/add-members/", views.AddHouseMember.as_view()
    ),
    path(
        "houses/<uuid:house_id>/add-members/search/",
        views.NonHouseMemberUserProfileSearch.as_view(),
    ),
    path("houses/", include(house_router.urls)),
]
