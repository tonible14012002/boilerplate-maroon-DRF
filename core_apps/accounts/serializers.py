from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'pkid', 'username', 'first_name', 'last_name', 'email', 'dob', 'phone']


class UserRegistrationSerializer(ModelSerializer):

    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'dob', 'phone', 'password', 'password_confirm']

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("Confirm password incorrect")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)

        user = User(
            **validated_data,
            # TODO: itegrate 2step auth through email
            # is_active=False
        )
        user.set_password(raw_password=password)
        return user
