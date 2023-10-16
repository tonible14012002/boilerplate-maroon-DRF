from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

stories_router = SimpleRouter()
stories_router.register('archieved', views.UserAchievedStory, 'archieved')
stories_router.register('following', views.FollowingStory, 'following')
stories_router.register('all', views.Story, 'story')

urlpatterns = [
    path('', include(stories_router.urls)),
]
