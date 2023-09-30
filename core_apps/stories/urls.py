from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    UserAchievedStoryViewset
)

stories_router = SimpleRouter()
stories_router.register('', UserAchievedStoryViewset, 'stories')

urlpatterns = [
    path('archieved/', include(stories_router.urls)),
    # path('stories/', )
]
