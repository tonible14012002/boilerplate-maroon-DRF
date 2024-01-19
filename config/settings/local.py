from .base import *  # noqa
from constants import config

DATABASES = {
    "default": config.DEFAULT_DATABASE_URL,
}
