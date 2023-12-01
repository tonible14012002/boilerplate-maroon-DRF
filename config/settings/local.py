from .base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", default="django-insecure-13nwtd72hax20!p+$e$_zo=(0y@e25q3qee0uwrjh)1mhq5q3o")  # noqa

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    # Add nginx origin
]
