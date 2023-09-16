from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet

router = SimpleRouter()
router.register("all", UserViewSet, "user")

urlpatterns = [
    path('', include(router.urls)),
]
