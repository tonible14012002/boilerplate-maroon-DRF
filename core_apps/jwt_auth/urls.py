from django.urls import path
from .views import MyTokenObtainPairView, MyTokenRefreshView


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view()),
    path('refresh/', MyTokenRefreshView.as_view())
]