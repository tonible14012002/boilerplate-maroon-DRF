import threading
from cassandra.cluster import Cluster
from django.conf import settings


thread_local = threading.local()


def get_session():
    if hasattr(thread_local, "cassandra_session"):
        return thread_local.cassandra_session
    return thread_local.cassandra_session


def new_cassandra_connection():
    cluster = Cluster([settings.DATABASES["cassandra"]["HOST"],], protocol_version=3)
    session = cluster.connect(settings.DATABASES["cassandra"]["NAME"])
    thread_local.cassandra_session = session
    return session


def close_cassandra_connection():
    session = thread_local.cassandra_session
    session.shutdown()
    thread_local.cassandra_session = None
