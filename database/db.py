import psycopg2
from psycopg2 import DatabaseError
import os

def get_connection():
    password_bb = os.getenv(password_bb)
    usuario_bb = os.getenv(usuario_bb)
    try:
        return psycopg2.connect(host='0.tcp.sa.ngrok.io',
                                user=usuario_bb,
                                password=password_bb,
                                database='pruebas',
                                port='14208')
    except DatabaseError as ex:
        raise ex
