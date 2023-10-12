from typing import Any
from django.contrib.auth import models
from django.contrib.auth.hashers import make_password


class UserManager(models.UserManager):
    def from_ids(self, *ids):
        return self.filter(id__in=ids)

    def create(self, **kwargs: Any) -> Any:
        password = kwargs.pop('password', None)
        assert bool(password)
        return super().create(
            password=make_password(password),
            **kwargs
        )
