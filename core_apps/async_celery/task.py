import threading
from celery.signals import worker_process_init, worker_process_shutdown
from . import db

thread_local = threading.local()


@worker_process_init.connect
def open_cassandra_session(*args, **kwargs):
    db.__new_cassandra_connection()


@worker_process_shutdown.connect
def close_cassandra_session(*args, **kwargs):
    db.__close_cassandra_connection()
