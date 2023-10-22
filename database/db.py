import psycopg2
from psycopg2 import DatabaseError
import os

def get_connection():
    password_bbdd = os.getenv('password_bbdd')
    usuario_bbdd = os.environ.get('usuario_bbdd')

    try:
        return psycopg2.connect(host='0.tcp.sa.ngrok.io',
                                user=password_bbdd,
                                password=usuario_bbdd,
                                database='pruebas',
                                port='14208')
    except DatabaseError as ex:
        raise ex
