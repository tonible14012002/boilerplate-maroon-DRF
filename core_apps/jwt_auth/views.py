# Create your views here.
from .serializers import MyTokenRefreshSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from core_apps.accounts.serializers import UserProfileSerializer


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProfileFromTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
