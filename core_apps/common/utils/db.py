from django.db import connections
from django.db.utils import load_backend


def cassandra_connection():
    db = connections.databases['cassandra']
    backend = load_backend(db['ENGINE'])
    return backend.DatabaseWrapper(db, 'cassandra')
