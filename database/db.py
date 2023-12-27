import psycopg2
from psycopg2 import DatabaseError
import os

def get_connection():
    password_bbdd = os.getenv('password_bbdd')
    usuario_bbdd = os.environ.get('usuario_bbdd')

    try:
        return psycopg2.connect(host='dpg-cl9u69u2eqrc7393iifg-a.oregon-postgres.render.com',
                                user=usuario_bbdd,
                                password=password_bbdd,
                                database='pruebas',
                                port='5432')
    except DatabaseError as ex:
        raise ex
