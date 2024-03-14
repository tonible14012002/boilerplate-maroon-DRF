# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core_apps.user import serializers as user_serializers

from . import serializers
from .serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProfileFromTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = user_serializers.ReadUpdateUserProfile(user)
        return Response(serializer.data)


class ProfileRegistration(CreateAPIView):
    serializer_class = serializers.RegisterUser
