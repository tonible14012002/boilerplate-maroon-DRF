from django.urls import include, path
from rest_framework import routers
from .views import (
    UserProfileViewset,
    ProfileRegistrationView,
    FollowUserView,
    UnFollowUserView,
    UserFollowingsView,
    UserFollowersView
)

profile_router = routers.DefaultRouter()

profile_router.register('', UserProfileViewset, "profile")

urlpatterns = [
    path('profile/registration/', ProfileRegistrationView.as_view()),
    path('profile/<uuid:uid>/follow/', FollowUserView.as_view()),
    path('profile/<uuid:uid>/unfollow/', UnFollowUserView.as_view()),
    path('profile/<uuid:uid>/followers/', UserFollowersView.as_view()),
    path('profile/<uuid:uid>/followings/', UserFollowingsView.as_view()),
    path('profile/', include(profile_router.urls)),
]
