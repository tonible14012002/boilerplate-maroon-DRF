# Add User Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from core_apps.accounts.serializers import UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(self.user).data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    pass
