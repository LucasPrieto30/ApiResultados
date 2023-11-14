from database.db import get_connection
from cryptography.fernet import Fernet
import psycopg2
from datetime import datetime
import os
import bcrypt

def cargar_clave_medico():
    with open("clave_medico.key", "rb") as archivo:
        return archivo.read()

def insert_medico(nuevo_medico):
    connection = get_connection()
    cursor = connection.cursor()
    clave_maestra = cargar_clave_medico()
    fernet = Fernet(clave_maestra)
    try:
        select_query = """
        INSERT INTO usuario (nombre, dni, email, password, rol_id, establecimiento_id, fecha_ultima_password, especialidad)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        correo_cifrado = fernet.encrypt(nuevo_medico.get("email").encode())  # Cifra solo el campo "email"

        cursor.execute(select_query, (
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
        return {"success": True, "message": "Usuario creado exitosamente"}
    except psycopg2.Error as e:
        # Captura la excepción específica de psycopg2.Error
        connection.rollback()
        return {"success": False, "message": "Error al crear el usuario: " + str(e)}
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
    clave_maestra= obtener_clave_desde_Medico()
    try:
        select_query = """
        SELECT id, nombre, dni, pgp_sym_decrypt(email::bytea, %s, 'compress-algo=0,cipher-algo=AES128') AS email_descifrado,
        password, rol_id, establecimiento_id, fecha_ultima_password, especialidad
        FROM usuario
        WHERE id = %s
        """
        cursor.execute(select_query, (clave_maestra, medico_id))
        medico_data = cursor.fetchone()
        if medico_data:
            if ', ' in medico_data[1]:
                apellido_usuario, nombre_usuario = medico_data[1].split(', ')
            else:
                apellido_usuario, nombre_usuario = '', medico_data[1]
            id = medico_data[0]
            nombre = nombre_usuario
            apellido = apellido_usuario
            dni = medico_data[2]
            email_descifrado = medico_data[3]
            #password = medico_data[4]
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

            medico = {
                "id": id,
                "nombre": nombre,
                "apellido": apellido,
                "dni": dni,
                "email": email_descifrado,
                #"password": password,
                "rol_id": rol_id,
                "establecimiento_id": establecimiento_id,
                "fecha_ultima_password": fecha_ultima_password_str,
                "especialidad": especialidad
            }
            return medico
        else:
            return {"message": "No se encontró ningún usuario con ese ID"}
    except Exception as e:
        connection.rollback()
        return {"success": False, "message": "Error inesperado: " + str(e)}
    finally:
        cursor.close()
        connection.close()


'''
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
def obtener_clave_desde_Medico():
        clave = os.environ.get('claveMedico')
        return clave
        '''
        try:
            with open('./etc/secrets/claveMedico.txt', 'r') as archivo:
                clave = archivo.read().strip()
                print(clave)
            return clave
        except FileNotFoundError:
            print(f"El archivo no se encontró.")
        except Exception as ex:
            print(f"Error al leer la clave desde el archivo: {ex}")
        return None
'''
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
def verificar_Usuario_rol_medico(valor):
    if valor == 4:
        conn = get_connection()       
        cur = conn.cursor()
        cur.execute("SELECT id, tipo, descripcion FROM public.rol WHERE id = 4")    
        resultado = cur.fetchone()
        conn.close()      
        # Verificar si se encontró un registro con id igual a 4 y tipo igual a "Medico"
        if resultado and resultado[0] == 4 and resultado[1] == "Medico":
            return True

    return False

def checkUsuarioPorDni(dni):
    clave_maestra= obtener_clave_desde_Medico()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, nombre, rol_id, dni, pgp_sym_decrypt(email::bytea, %s, 'compress-algo=0,cipher-algo=AES128') AS email, password, especialidad, establecimiento_id, fecha_ultima_password FROM public.usuario where dni = %s", (clave_maestra, dni,))
    usuarioBD = cursor.fetchone()
    if usuarioBD:
        return usuarioBD
    else:
        return None

def verificarPassword(password, usuarioExistente):
    if len(usuarioExistente) > 5:
        # Codifica la contraseña en bytes antes de usar bcrypt.checkpw
        recovered_password = bytes.fromhex(usuarioExistente[5][2:])
        password_encoded = password.encode('utf-8')
        # Usa bcrypt.checkpw para verificar la contraseña
        return bcrypt.checkpw(password_encoded, recovered_password)
        # Verifica si la contraseña coincide
    else:
        return False
def get_ultimo_cambio_pass(dni): 
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("""SELECT fecha_ultima_password FROM public."usuario" WHERE dni=%s;""", (dni,)) 
        result = cursor.fetchone()
        cursor.close() 

    if result is not None:
        return result[0] 
    return None

def guardar_codigo(codigo, dni):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE public.usuario SET verify_code=%s WHERE dni=%s;""", (codigo,dni,))
            connection.commit()
            return True
    except Exception as e:
        connection.rollback()
        return {"success": False, "message": "Error inesperado: " + str(e)}
    finally:
        connection.close()

def borrar_codigo(dni):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE public.usuario SET verify_code=NULL WHERE dni=%s;""", (dni,))
            connection.commit()
            return True
    except Exception as e:
        connection.rollback()
        return {"success": False, "message": "Error inesperado: " + str(e)}
    finally:
        connection.close()

def set_code(codigo, dni):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE public.usuario SET reset_code=%s, reset_code_timestamp = NOW() WHERE dni=%s;""", (codigo,dni,))
            connection.commit()
            return True
    except Exception as e:
        connection.rollback()
        return {"success": False, "message": "Error inesperado: " + str(e)}
    finally:
        connection.close() 
        
def checkUsuarioPorDni_reset(dni):
    connection = get_connection()
    cursor = connection.cursor()
    #cursor.execute("SELECT id, nombre, rol_id, dni, pgp_sym_decrypt(email::bytea, %s, 'compress-algo=0,cipher-algo=AES128') AS email, password, especialidad, establecimiento_id, fecha_ultima_password FROM public.usuario where dni = %s", (dni,))
    cursor.execute("""
    SELECT 
        id, nombre, rol_id, dni, 
        pgp_sym_decrypt(email::bytea, 'q[Ia=wwY=1goiRR') AS email, 
        password, especialidad, establecimiento_id, fecha_ultima_password 
    FROM public.usuario 
    WHERE dni = %s
    """, (dni,))

    usuarioBD = cursor.fetchone()
    if usuarioBD:
        return usuarioBD
    else:
        return None
    
def identify_user_by_reset_token(reset_token):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT dni FROM public.usuario where reset_token = %s", ( reset_token,))
    usuarioBD = cursor.fetchone()
    if usuarioBD:
        return usuarioBD[0]
    else:
        return None

def reset_user_password(reset_token, new_password):
    password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE public.usuario SET reset_code = NULL,reset_token = NULL, password = %s WHERE reset_token = %s;", (password_hash, reset_token,))
    connection.commit()
    connection.close()
