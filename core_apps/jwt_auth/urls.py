from django.urls import path
from .views import MyTokenObtainPairView, MyTokenRefreshView, ProfileFromTokenView


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view()),
    path('refresh/', MyTokenRefreshView.as_view()),
    path('profile/', ProfileFromTokenView.as_view()),
]
