import environ
from pathlib import Path

env = environ.Env()


# local | production
BUILD_ENVIRONMENT = env.str('BUILD_ENVIRONMENT', 'local')

ROOT_DIR = Path(__file__).resolve().parent.parent

DEFAULT_DATABASE_URL = env.db("DATABASE_URL", f"sqlite:///{ROOT_DIR}/db.sqlite3")

CELERY_BROKER_URL = env.str('BROKER_URL', 'amqp://guest:guest@rabbitmq:5672/')

DEBUG = env.bool('DJANGO_DEBUG', True)
SECRET_KEY = env("DJANGO_SECRET_KEY", default="django-insecure-13nwtd72hax20!p+$e$_zo=(0y@e25q3qee0uwrjh)1mhq5q3o")
