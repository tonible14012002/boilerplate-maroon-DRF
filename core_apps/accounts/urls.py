from django.urls import include, path
from rest_framework import routers
from . import views


profile_router = routers.DefaultRouter()

profile_router.register('', views.UserProfileViewset, "profile")

urlpatterns = [
    path('profile/registration/', views.ProfileRegistration.as_view()),
    path('profile/<uuid:uid>/follow/', views.UserFollowers.as_view()),
    path('profile/<uuid:uid>/unfollow/', views.UnFollowUser.as_view()),
    path('profile/<uuid:uid>/followers/', views.FollowUser.as_view()),
    path('profile/<uuid:uid>/followings/', views.UserFollowings.as_view()),
    path('profile/', include(profile_router.urls)),
]
