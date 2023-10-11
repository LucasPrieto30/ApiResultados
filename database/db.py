import psycopg2
from psycopg2 import DatabaseError

def get_connection():
    try:
        return psycopg2.connect(host='0.tcp.sa.ngrok.io',
                                user='mica',
                                password=1234,
                                database='pruebas',
                                port='15360')
    except DatabaseError as ex:
        raise ex
