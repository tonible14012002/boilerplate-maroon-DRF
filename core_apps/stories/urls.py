from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

stories_router = SimpleRouter()
stories_router.register('archieved', views.UserAchievedStoryViewset, 'archieved')  # expired
stories_router.register('following', views.FollowingStoryViewset, 'following')  # Expired
stories_router.register('all', views.Story, 'story')  # Test only

urlpatterns = [
    path('', include(stories_router.urls)),
    path('new/', views.PostStory.as_view())
]
