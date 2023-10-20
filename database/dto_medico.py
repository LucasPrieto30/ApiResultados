from database.db import get_connection
from cryptography.fernet import Fernet
import psycopg2

def cargar_clave_medico():
    with open("clave_medico.key", "rb") as archivo:
        return archivo.read()

def insert_medico(nuevo_medico):
    connection = get_connection()
    cursor = connection.cursor()
    clave_maestra = cargar_clave_medico()
    fernet = Fernet(clave_maestra)
    try:
        insert_query = """
        INSERT INTO usuario (id, nombre, dni, email, password, rol_id, establecimiento_id, fecha_ultima_password, especialidad)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        correo_cifrado = fernet.encrypt(nuevo_medico.get("email").encode())  # Cifra solo el campo "email"

        cursor.execute(insert_query, (
            nuevo_medico.get("id"),
            nuevo_medico.get("nombre"),
            nuevo_medico.get("dni"),
            correo_cifrado,
            nuevo_medico.get("password"),
            nuevo_medico.get("rol_id"),
            nuevo_medico.get("establecimiento_id"),
            nuevo_medico.get("fecha_ultima_password"),
            nuevo_medico.get("especialidad")
        ))
        connection.commit()
        return {"success": True, "message": "Medico creado exitosamente"}
    except psycopg2.Error as e:
        # Captura la excepción específica de psycopg2.Error
        connection.rollback()
        return {"success": False, "message": "Error al crear el medico: " + str(e)}
    except Exception as e:
        connection.rollback()
        #raise e
        return {"success": False, "message": "Error inesperado: " + str(e)}
    finally:
        cursor.close()
        connection.close()
