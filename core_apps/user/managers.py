from typing import Any

from django.contrib.auth import models
from django.contrib.auth.hashers import make_password
from django.db.models.query import QuerySet


class UserManager(models.UserManager):
    def from_ids(self, *ids):
        return self.filter(id__in=ids)

    def create(self, **kwargs: Any) -> Any:
        password = kwargs.pop("password", None)
        assert bool(password)
        return super().create(password=make_password(password), **kwargs)

    def order_by_join_day(self, ascendent=False):
        if ascendent:
            return self.get_queryset().order_by("-date_joined")
        else:
            return self.get_queryset().order_by("date_joined")


class TestUserManager(UserManager):
    def get_queryset(self) -> QuerySet:
        return super(TestUserManager, self).get_queryset().filter(is_test=True)

    def create(self, **kwargs: Any) -> Any:
        kwargs["is_test"] = True
        return super(TestUserManager, self).create(**kwargs)
