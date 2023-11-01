import psycopg2
from psycopg2 import DatabaseError
import os

def get_connection():
    password_bbdd = os.getenv('password_bbdd')
    usuario_bbdd = os.environ.get('usuario_bbdd')

    try:
        return psycopg2.connect(host='dpg-cktdoceb0mos73btj9g0-a.oregon-postgres.render.com',
                                user='nahuel',
                                password='JejesARlfvkXh30LVIeMTV4FD0O26gvT',
                                database='backup_2wug',
                                port='5432')
    except DatabaseError as ex:
        raise ex
