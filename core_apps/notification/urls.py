from django.urls import path
from . import views as notification_views


urlpatterns = [
    # House notifications
    path(
        "room/<uuid:room_id>/",
        notification_views.RoomNotification.as_view(),
    ),
    # Room notifications
    path(
        "house/<uuid:house_id>/",
        notification_views.HouseNotification.as_view(),
    ),
]
