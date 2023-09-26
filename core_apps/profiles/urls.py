from django.urls import include, path
from rest_framework import routers
from .views import (
    UserProfileViewset,
    ProfileRegistrationView
)

profile_router = routers.DefaultRouter()

profile_router.register('profile', UserProfileViewset, "profile")

urlpatterns = [
    path('profile/registration/', ProfileRegistrationView.as_view(), name="registration"),
    path('', include(profile_router.urls), name="profile-viewset"),
]
