from django.db import connections
from core_apps.async_celery import db
import environ

env = environ.Env()


def cassandra_connection():
    if not env.bool("IS_CELERY_WORKER", False):
        return connections['cassandra']
    return db.get_session()
