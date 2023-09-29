from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    UserStoryViewset
)

stories_router = SimpleRouter()
stories_router.register('', UserStoryViewset, 'stories')

urlpatterns = [
    path('archieved/', include(stories_router.urls))
]
