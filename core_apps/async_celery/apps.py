from django.apps import AppConfig


class AsyncCeleryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.async_celery"
