from django.db import connections


def db_connection(dbname: str):
    try:
        return connections.get(dbname)
    except KeyError:
        raise Exception(f'Database {dbname} notfound')
