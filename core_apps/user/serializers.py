from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from . import models

User: models.MyUser = get_user_model()
Profile = models.Profile


class ReadBasicUserProfile(ModelSerializer):
    avatar = serializers.URLField(source="profile.avatar")
    nickname = serializers.CharField(source="profile.nickname")

    class Meta:
        model = User
        fields = [
            "id",
            "avatar",
            "nickname",
            "first_name",
            "last_name",
        ]


class ReadUpdateUserProfile(ModelSerializer):
    fullname = serializers.CharField(source="get_fullname", read_only=True)

    # Profile fields -> data['profile']
    avatar = serializers.URLField(source="profile.avatar", default="")
    gender = serializers.CharField(source="profile.gender", default="")
    city = serializers.CharField(source="profile.city", default="")
    country = serializers.CharField(source="profile.country", default="")
    nickname = serializers.CharField(source="profile.nickname", default="")

    class Meta:
        USER_FIELDS = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "dob",
            "phone",
        ]
        USER_EXTRA_FIELDS = [
            "fullname",
        ]
        PROFILE_FIELDS = ["avatar", "gender", "city", "country", "nickname"]
        model = User
        fields = PROFILE_FIELDS + USER_FIELDS + USER_EXTRA_FIELDS
        read_only_fields = ["username", "email"]

    def update(self, user: models.MyUser, validated_data: dict):
        profile: models.Profile = user.profile
        profile_data = validated_data.pop("profile", {})
        user_data = validated_data

        profile.update_field(
            city=profile_data.get("city", None),
            nickname=profile_data.get("nickname", None),
            gender=profile_data.get("gender", None),
            avatar=profile_data.get("avatar", None),
        )

        user.update_field(
            first_name=user_data.get("first_name", None),
            last_name=user_data.get("last_name", None),
            dob=user_data.get("dob", None),
            phone=user_data.get("phone", None),
        )

        return user
