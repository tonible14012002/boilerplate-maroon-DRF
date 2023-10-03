from django.contrib.auth.models import BaseUserManager
from django.apps import apps
from django.contrib.auth.hashers import make_password


class AccountManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        profile_fields = extra_fields.pop('profile', {})

        user = self.create_user_instance(
            username,
            email,
            password,
            **extra_fields
        )
        self.create_profile_instance(user, **profile_fields)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(username, email, password, **extra_fields)

    def create_user_instance(self, username, email, password, **fields):
        if not username:
            raise ValueError("The given username must be set")

        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        # Create user instance
        user = self.model(
            username,
            email,
            **fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_profile_instance(self, user, **extra_fields):
        profile_model = apps.get_model(
            self.model.app_label,
            'Profile'
        )
        return profile_model.objects.create(
            user=user,
            **extra_fields
        )
