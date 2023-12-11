from django.db import connections


def cassandra_connection():
    return connections['cassandra']
