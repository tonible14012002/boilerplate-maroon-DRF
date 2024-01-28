from django.urls import path, include
from rest_framework import routers
from . import views

house_router = routers.DefaultRouter()
house_router.register("", views.HouseViewset, "houses")

urlpatterns = [
    path("houses/", include(house_router.urls)),
]
