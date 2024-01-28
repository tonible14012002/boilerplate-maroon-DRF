from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest

User = get_user_model()


class PhoneBackend(ModelBackend):
    def authenticate(
        self,
        request: HttpRequest,
        username: str | None = ...,
        password: str | None = ...,
        **kwargs: Any
    ) -> AbstractBaseUser | None:
        try:
            user = User.objects.get(phone=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
