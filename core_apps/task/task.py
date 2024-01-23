from celery.signals import worker_process_init, worker_process_shutdown


@worker_process_init.connect
def connect_db(**_):
    # Reconnect database
    pass


@worker_process_shutdown.connect
def disconnect(**_):
    pass
