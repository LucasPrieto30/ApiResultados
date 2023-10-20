from database.db import get_connection
from cryptography.fernet import Fernet
import psycopg2
from datetime import datetime

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


def consultar_medico_id(medico_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        select_query = """
        SELECT id, nombre, dni, email, password, rol_id, establecimiento_id, fecha_ultima_password, especialidad
        FROM usuario
        WHERE id = %s
        """
        cursor.execute(select_query, (medico_id,))
        medico_data = cursor.fetchone()
        clave_maestra = cargar_clave_medico()
        fernet = Fernet(clave_maestra)
        if medico_data:
            id = medico_data[0]
            nombre = medico_data[1]
            dni = medico_data[2]
            password = medico_data[4]
            rol_id = medico_data[5]
            establecimiento_id = medico_data[6]
            fecha_ultima_password = medico_data[7]
            especialidad = medico_data[8]

            if fecha_ultima_password is not None:
                # Convierte la fecha a una cadena en un formato deseado (por ejemplo, "Año-Mes-Día Hora:Minuto:Segundo")
                fecha_ultima_password_str = fecha_ultima_password.strftime("%Y-%m-%d %H:%M:%S")
            else:
                # Establece una cadena predeterminada o un valor apropiado cuando fecha_ultima_password es None
                fecha_ultima_password_str = "Fecha no disponible"
            try:
                correo_cifrado_bytes = bytes(medico_data[3])  # Asegura que sea bytes
             
                correo_descifrado = fernet.decrypt(correo_cifrado_bytes)
            except Exception as e:
                connection.rollback()
                return {"success": False, "message": "Error al desencriptar el correo: " + str(e)}
            medico = {
                "id": id,
                "nombre": nombre,
                "dni": dni,
                "email": correo_descifrado.decode('utf-8'),
                "password": password,
                "rol_id": rol_id,
                "establecimiento_id": establecimiento_id,
                "fecha_ultima_password": fecha_ultima_password_str,
                "especialidad": especialidad
            }
            return {"success": True, "medico": medico}
        else:
            return {"success": True, "message": "No se encontró ningún médico con ese ID"}

    except Exception as e:
        connection.rollback()
        if "Error al desencriptar" in str(e):
            return {"success": False, "message": str(e)}
        else: 
            return {"success": False, "message": "Error inesperadooo: " + str(e)}
    finally:
        cursor.close()
        connection.close()
'''
def consultar_medico_id(medico_id):    
        # Realizar la consulta en la base de datos para obtener los datos del médico por su ID
        connection = get_connection()
        cursor = connection.cursor()
        try:
            select_query = """
            SELECT id, nombre, dni, email, password, rol_id, establecimiento_id, fecha_ultima_password, especialidad
            FROM usuario
            WHERE id = %s
            """
            cursor.execute(select_query, (medico_id,))
            medico_data = cursor.fetchone()
            clave_maestra = cargar_clave_medico()
            fernet = Fernet(clave_maestra)
            if medico_data:
                # Los datos del médico se encuentran en medico_data
                id = medico_data[0]
                nombre = medico_data[1]
                dni = medico_data[2]
                password = medico_data[4]
                rol_id = medico_data[5]
                establecimiento_id = medico_data[6]
                fecha_ultima_password = medico_data[7]
                especialidad = medico_data[8]
                #correo_cifrado = medico_data[2]
                #contrasena_cifrada = medico_data[3]
                #correo_cifrado_hex = correo_cifrado
                #contrasena_cifrada_hex = contrasena_cifrada
                #correo_cifrado_bytes = bytes.fromhex(correo_cifrado_hex[2:])
                #contrasena_cifrada_bytes = bytes.fromhex(contrasena_cifrada_hex[2:])
                # Cargar la clave maestra desde el archivo
                correo_cifrado_bytes = bytes(medico_data[3])  # Asegura que sea bytes
                #clave_maestra = cargar_clave_medico()
                    # Crear una instancia de Fernet con la clave maestra
                #fernet = Fernet(clave_maestra)
                # Desencriptar los datos
                correo_descifrado = fernet.decrypt(correo_cifrado_bytes)

                #correo_descifrado = desencriptar_valor(correo_cifrado,clave_maestra)
                #contrasena_descifrada = desencriptar_valor(contrasena_cifrada,clave_maestra)
                medico = {
                    "id": id,
                    "nombre": nombre,
                    "dni": dni,
                    "email": correo_descifrado,
                    "password": password,
                    "rol_id": rol_id,
                    "establecimiento_id": establecimiento_id,
                    "fecha_ultima_password": fecha_ultima_password,
                    "especialidad": especialidad
                    #"correo":fernet.decrypt(correo_cifrado).decode(),
                    #"contrasena": fernet.decrypt(contrasena_cifrada).decode()
                }
                #correo_legible = fernet.decrypt(medico["correo_electronico"]).decode()
                #contrasena_legible = fernet.decrypt(medico["contrasena"]).decode()
                #print(correo_legible)
                #print(contrasena_legible)
                return {"success": True, "medico": medico}
        else:
            return {"success": True, "message": "No se encontró ningún médico con ese ID"}

    except Exception as e:
        connection.rollback()
        return {"success": False, "message": "Error inesperado: " + str(e)}
    finally:
        cursor.close()
        connection.close()

'''