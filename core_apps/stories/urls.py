from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

stories_router = SimpleRouter()
stories_router.register('archieved', views.UserAchievedStory, 'archieved')  # expired
stories_router.register('following', views.FollowingStory, 'following')  # Expired
stories_router.register('all', views.Story, 'story')  # Test only

urlpatterns = [
    path('', include(stories_router.urls)),
]
