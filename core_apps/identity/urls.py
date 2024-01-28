from django.urls import path

from . import views

urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view()),
    path("refresh/", views.MyTokenRefreshView.as_view()),
    path("me/", views.ProfileFromTokenView.as_view()),
    path("registration/", views.ProfileRegistration.as_view()),
]
