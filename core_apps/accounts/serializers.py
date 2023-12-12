from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import ValidationError
from . import models

User: models.MyUser = get_user_model()
Profile = models.Profile


class ReadBasicUserProfile(ModelSerializer):
    avatar = serializers.URLField(source='profile.avatar')
    nickname = serializers.CharField(source='profile.nickname')
    is_followed = serializers.SerializerMethodField(method_name='check_is_followed')

    def check_is_followed(self, instance):
        request = self.context.get('request', None)
        if (
            request
            and request.user.is_authenticated
            and request.user.pkid != instance.pkid
        ):
            return request.user.is_following_user(instance)
        return None

    class Meta:
        model = User
        fields = ['id', 'avatar', 'nickname', 'first_name', 'last_name', 'total_followers', 'is_followed']


class ReadUpdateUserProfile(ModelSerializer):

    fullname = serializers.CharField(source='get_fullname', read_only=True)

    # Profile fields -> data['profile']
    avatar = serializers.URLField(source='profile.avatar', default="")
    gender = serializers.CharField(source='profile.gender', default="")
    city = serializers.CharField(source='profile.city', default="")
    country = serializers.CharField(source='profile.country', default="")
    nickname = serializers.CharField(source='profile.nickname', default="")
    is_followed = serializers.SerializerMethodField(method_name='check_is_followed')

    class Meta:
        USER_FIELDS = [
            'id', 'username', 'first_name', 'last_name', 'email', 'dob', 'phone'
        ]
        USER_EXTRA_FIELDS = ['total_followers', 'fullname', 'total_followings']
        PROFILE_FIELDS = ['avatar', 'gender', 'city', 'country', 'nickname']
        EXTRA_FIELDS = ['is_followed']

        model = User
        fields = PROFILE_FIELDS + USER_FIELDS + USER_EXTRA_FIELDS + EXTRA_FIELDS
        read_only_fields = ['username', 'email', 'total_followers', 'total_followings'] + EXTRA_FIELDS

    def check_is_followed(self, instance):
        request = self.context.get('request', None)
        if (
            request
            and request.user.is_authenticated
            and request.user.pkid != instance.pkid
        ):
            return request.user.is_following_user(instance)
        return None

    def update(self, user: models.MyUser, validated_data: dict):
        profile: models.Profile = user.profile
        profile_data = validated_data.pop('profile', {})
        user_data = validated_data

        profile.update_field(
            city=profile_data.get('city', None),
            nickname=profile_data.get('nickname', None),
            gender=profile_data.get('gender', None),
            avatar=profile_data.get('avatar', None),
        )

        user.update_field(
            first_name=user_data.get('first_name', None),
            last_name=user_data.get('last_name', None),
            dob=user_data.get('dob', None),
            phone=user_data.get('phone', None),
        )

        return user


class RegisterUser(ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    gender = serializers.CharField(source='profile.gender', required=False)
    city = serializers.CharField(source='profile.city', required=False)
    country = serializers.CharField(source='profile.country', required=False)
    avatar = serializers.URLField(source='profile.avatar', required=False)

    class Meta:
        PROFILE_FIELDS = ['gender', 'country', 'city', 'avatar']
        USER_FIELDS = ['id', 'username', 'first_name', 'last_name', 'email', 'dob', 'phone']

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
            raise ValidationError('Confirm password incorrect')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        profile_data = validated_data.pop('profile', {})
        user = User.create_register(
            username=validated_data.pop('username'),
            password=validated_data.pop('password'),
            extra_fields=validated_data,
            profile_fields=profile_data
        )
        return user
