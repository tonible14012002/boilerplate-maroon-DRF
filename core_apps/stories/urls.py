from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    UserAchievedStoryViewset,
    FriendStoryViewset
)

stories_router = SimpleRouter()
stories_router.register('archieved', UserAchievedStoryViewset, 'archieved')
stories_router.register('following', FriendStoryViewset, 'following')

urlpatterns = [
    path('', include(stories_router.urls)),
]
