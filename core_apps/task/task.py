from celery.signals import worker_process_init, worker_process_shutdown
from django.db import connections


@worker_process_init.connect
def connect_db(**_):
    connections['cassandra'].reconnect()


@worker_process_shutdown.connect
def disconnect(**_):
    connections['cassandra'].close_all()
