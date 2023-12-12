from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

stories_router = SimpleRouter()

stories_router.register('archieved', views.UserAchievedStoryViewset, 'archieved'),  # expired
stories_router.register('stories', views.StoryViewSet)

urlpatterns = [
    path('stories/<uuid:uid>/view/', views.ViewStory.as_view()),
    path('', include(stories_router.urls)),
    path('new/', views.PostStory.as_view()),
    path('following/', views.AllFollowingStory.as_view()),
]
