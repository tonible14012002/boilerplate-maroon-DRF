from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Profile

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'dob', 'phone']


class SimpleProfileSerializer(ModelSerializer):
    avatar = serializers.URLField(source='profile.avatar')
    nickname = serializers.CharField(source='profile.nickname')

    class Meta:
        model = User
        fields = ['id', 'avatar', 'nickname', 'first_name', 'last_name']


class UserProfileSerializer(ModelSerializer):

    total_followers = serializers.SerializerMethodField(method_name='get_total_followers', default='')
    total_followings = serializers.SerializerMethodField(method_name='get_total_followings', default='')
    fullname = serializers.SerializerMethodField(method_name='get_fullname')
    avatar = serializers.URLField(source='profile.avatar')
    gender = serializers.CharField(source='profile.gender')
    city = serializers.CharField(source='profile.city')
    country = serializers.CharField(source='profile.country')
    nickname = serializers.CharField(source='profile.nickname')

    class Meta:
        PROFILE_FIELDS = ['gender', 'country', 'city', 'avatar', 'nickname']
        USER_FIELDS = [
            'id', 'username', 'first_name', 'last_name', 'email', 'dob',
            'dob', 'phone'
        ]
        model = User
        fields = PROFILE_FIELDS + USER_FIELDS + ['total_followers', 'fullname', 'total_followings']

    def get_total_followings(self, instance):
        return instance.followings.count()

    def get_total_followers(self, instance):
        return instance.followers.count()

    def get_fullname(self, instance):
        return instance.get_full_name()

    def to_representation(self, instance):
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)

        return super().to_representation(instance)

    def update(self, instance, validated_data):
        user = instance
        profile_data = validated_data.pop('profile', {})
        user.update_profile(**profile_data)
        user.update(**validated_data)
        return user


class UserRegistrationSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    gender = serializers.CharField(source='profile.gender', required=False)
    city = serializers.CharField(source='profile.city', required=False)
    country = serializers.CharField(source='profile.country', required=False)
    avatar = serializers.URLField(source='profile.avatar', required=False)

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
            raise ValidationError('Confirm password incorrect')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        profile_data = validated_data.pop('profile', {})
        user = User.manager.create_user(
            **validated_data,
            profile=profile_data
        )
        return user


class UserFollowerSerializer():
    followers = SimpleProfileSerializer(
        many=True,
        read_only=True
    )
    include_fields = ['followers']


class UserFollowingSerializer():
    followings = SimpleProfileSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        fields = ['followings']
