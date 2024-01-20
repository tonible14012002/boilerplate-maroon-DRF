# Create your views here.
from .serializers import MyTokenRefreshSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from . import serializers


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProfileFromTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = serializers.ReadUpdateUserProfile(user)
        return Response(serializer.data)


class ProfileRegistration(CreateAPIView):
    serializer_class = serializers.RegisterUser
