from django.urls import include, path
from rest_framework import routers
from . import views


profile_router = routers.DefaultRouter()

profile_router.register('', views.UserProfileViewset, "profile")

urlpatterns = [
    path('profile/search/', views.UserProfileSearch.as_view()),
    path('profile/ids/', views.UserProfileByIds.as_view()),
    path('profile/', include(profile_router.urls)),
    path('profile/delete/', views.DeleteUserProfile.as_view()),
    path('profile/<uuid:uid>/follow/', views.FollowUser.as_view()),
    path('profile/<uuid:uid>/unfollow/', views.UnFollowUser.as_view()),
    path('profile/<uuid:uid>/followers/', views.UserFollowers.as_view()),
    path('profile/<uuid:uid>/followings/', views.UserFollowings.as_view()),
]
