# Add User Serializer
from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from core_apps.profiles.serializers import UserProfileSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data['user'] = UserProfileSerializer(self.user).data
        return data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    pass
