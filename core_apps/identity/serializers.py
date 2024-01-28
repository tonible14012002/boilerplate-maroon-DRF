# Add User Serializer
from typing import Any, Dict

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from core_apps.user import serializers as user_serializers

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data["user"] = user_serializers.ReadUpdateUserProfile(self.user).data
        return data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    pass


class RegisterUser(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    gender = serializers.CharField(source="profile.gender", required=False)
    city = serializers.CharField(source="profile.city", required=False)
    country = serializers.CharField(source="profile.country", required=False)
    avatar = serializers.URLField(source="profile.avatar", required=False)

    class Meta:
        PROFILE_FIELDS = ["gender", "country", "city", "avatar"]
        USER_FIELDS = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "dob",
            "phone",
        ]

        model = User
        fields = USER_FIELDS + PROFILE_FIELDS + ["password_confirm", "password"]
        extra_kwargs = {"dob": {"required": False}}

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")
        if password != password_confirm:
            raise ValidationError("Confirm password incorrect")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        profile_data = validated_data.pop("profile", {})
        user = User.create_register(
            username=validated_data.pop("username"),
            password=validated_data.pop("password"),
            extra_fields=validated_data,
            profile_fields=profile_data,
        )
        return user
