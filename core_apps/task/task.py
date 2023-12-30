from celery.signals import worker_process_init, worker_process_shutdown
import utils


@worker_process_init.connect
def connect_db(**_):
    utils.db_connection('cassandra').reconnect()


@worker_process_shutdown.connect
def disconnect(**_):
    utils.db_connection('cassandra').close_all()
