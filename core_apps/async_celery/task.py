from celery.signals import worker_process_init, worker_process_shutdown
from core_apps.common.utils import db as common_db_utils


@worker_process_init.connect
def connect_db(**_):
    common_db_utils.cassandra_connection().reconnect()


@worker_process_shutdown.connect
def disconnect(**_):
    common_db_utils.cassandra_connection().close_all()
