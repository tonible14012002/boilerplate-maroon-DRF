from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserProfileSerializer(ModelSerializer):

    total_followers = serializers.SerializerMethodField(method_name="get_total_followers", default="")
    fullname = serializers.SerializerMethodField(method_name='get_fullname')
    avatar = serializers.ImageField(source="profile.avatar")
    gender = serializers.CharField(source="profile.gender")
    city = serializers.CharField(source="profile.city")
    country = serializers.CharField(source="profile.country")

    class Meta:
        PROFILE_FIELDS = ['gender', 'country', 'city', 'avatar']
        USER_FIELDS = [
            'id', 'username', 'first_name', 'last_name', 'email', 'dob',
            'dob', 'phone'
        ]
        model = User
        fields = PROFILE_FIELDS + USER_FIELDS + ['total_followers', 'fullname']

    def get_total_followers(self, instance):
        return instance.profile.followers.count()

    def get_fullname(self, instance):
        return instance.get_full_name()

    def to_representation(self, instance):
        if not hasattr(instance, "profile"):
            Profile.objects.create(user=instance)

        return super().to_representation(instance)


class UserRegistrationSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    gender = serializers.CharField(source="profile.gender", required=False)
    city = serializers.CharField(source="profile.city", required=False)
    country = serializers.CharField(source="profile.country", required=False)
    avatar = serializers.ImageField(source="profile.avatar", required=False)

    class Meta:
        PROFILE_FIELDS = ['gender', 'country', 'city', 'avatar']
        USER_FIELDS = [
            'id', 'username', 'first_name', 'last_name', 'email', 'dob',
            'dob', 'phone',
        ]

        model = User
        fields = USER_FIELDS + PROFILE_FIELDS + ['password_confirm', 'password']
        extra_kwargs = {
            'phone': {
                'required': False
            },
            'dob': {
                'required': False
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("Confirm password incorrect")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password')
        validated_data.pop('password_confirm')
        profile_data = validated_data.pop('profile')

        user = User.objects.create(
            **validated_data
        )
        profile = Profile.objects.create(
            **profile_data,
            user=user
        )
        user.save()
        profile.save()

        password = validated_data.pop('password', None)
        user.set_password(raw_password=password)
        return user
