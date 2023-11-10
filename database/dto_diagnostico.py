
import base64
from database.db import get_connection
from psycopg2.extras import RealDictCursor
from database.dto_medico import obtener_clave_desde_Medico
# insertar diagnostico de modelo: cerebro
def insert_diagnostico(datos_diagnostico):
    clave_maestra=obtener_clave_desde_Medico()
    try:
        connection = get_connection()
        clave_maestra=obtener_clave_desde_Medico()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM usuario WHERE dni = %s", (datos_diagnostico.get("dni_medico"),))
            medicoExiste = cursor.fetchone()
            cursor.execute("SELECT pgp_sym_encrypt(%s, %s, 'compress-algo=0,cipher-algo=AES128');", (datos_diagnostico.get("datos_paciente"), clave_maestra))
            datos_paciente_encriptado = cursor.fetchone()[0]
            insert_query = """
            INSERT INTO public.diagnostico(imagen_id, datos_complementarios, fecha, resultado, usuario_id, modelo_id, usuario_medico_dni, usuario_medico_id, datos_paciente)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """
            values = (
                datos_diagnostico.get("imagen_id"),
                datos_diagnostico.get("datos_complementarios"),
                datos_diagnostico.get("fecha"),
                datos_diagnostico.get("resultado"),
                datos_diagnostico.get("usuario_id"),
                datos_diagnostico.get("id_modelo"),
                datos_diagnostico.get("dni_medico"),
                medicoExiste[0] if medicoExiste else None,
                datos_paciente_encriptado
            )
            cursor.execute("INSERT INTO public.imagen_analisis (imagen_id, imagen) VALUES (%s, %s);", (datos_diagnostico.get("imagen_id"), datos_diagnostico.get("imagen")))
            cursor.execute(insert_query, values)
            new_diagnostico_id = cursor.fetchone()[0]
            connection.commit()
            return new_diagnostico_id
    except Exception as e:
        connection.rollback()
        return {'error': str(e)}

def obtener_diagnostico(id_diagnostico, rol):
    diagnostico = None
    clave_maestra = obtener_clave_desde_Medico()
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT d.id, d.imagen_id, d.datos_complementarios, d.fecha, d.resultado, d.usuario_id, d.usuario_medico_dni, d.modelo_id, u.nombre as nombre_usuario, mo.nombre as modelo_nombre, me.nombre as nombre_medico, i.imagen as imagen, d.datos_paciente FROM Diagnostico as d INNER JOIN public.usuario as u ON d.usuario_id = u.id INNER JOIN public.imagen_analisis as i ON d.imagen_id = i.imagen_id INNER JOIN public.modelo as mo ON mo.id = d.modelo_id LEFT JOIN public.usuario as me ON d.usuario_medico_dni = me.dni WHERE d.id=%s;', (id_diagnostico,))
            
            row = cursor.fetchone()
            if(row is None):
                return None
            imagen_decodificada =  base64.b64decode(row[11])
            imagen_base64 = base64.b64encode(imagen_decodificada).decode('utf-8')

            if row is not None:
                if ', ' in row[8]:
                    apellido_usuario, nombre_usuario = row[8].split(', ')
                else:
                    apellido_usuario, nombre_usuario = '', row[8]

                if ', ' in  row[10]:
                    apellido_medico, nombre_medico=  row[10].split(', ')
                else:
                    apellido_medico, nombre_medico = '',  row[10]
                diagnostico = {
                    "id": row[0],  
                    "imagen_id": row[1],
                    "datos_complementarios": row[2],
                    "fecha": row[3].strftime("%Y-%m-%d %H:%M:%S"),
                    #"resultado": row[4],
                    "usuario_id": row[5],
                    "usuario_medico_dni": row[6],
                    "modelo_id": row[7],
                    "nombre_usuario": nombre_usuario,
                    "apellido_usuario": apellido_usuario,
                    "modelo_nombre": row[9],
                    "nombre_medico": nombre_medico,
                    "apellido_medico": apellido_medico,
                    "imagen": imagen_base64
                    #"datos_paciente": row[12]
                }
                if int(rol) == 4 or int(rol) == 1:
                    diagnostico["resultado"] = row[4]
                # Verificar y descifrar datos_paciente si está cifrado
                if row[12] is not None and row[12].startswith('\\x'):
                    cursor.execute(f"SELECT pgp_sym_decrypt('{row[12]}'::bytea, %s, 'compress-algo=0,cipher-algo=AES128');", (clave_maestra,))
                    datos_paciente_descifrado = cursor.fetchone()[0]
                    diagnostico["datos_paciente"] = datos_paciente_descifrado
            connection.close()
            connection.close()
        if diagnostico:
            return diagnostico
        else:
            return {"message": "Diagnóstico no encontrado"}
    except Exception as ex:
        return {"error" : "Error al obtener el diagnóstico"}, 500
    
def obtener_todos_diagnosticos():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_diagnostico, UsuarioId, Edad, Peso, AlturaCM, Sexo, SeccionCuerpo, CondicionesPrevias, Imagen FROM Diagnostico")
            rows = cursor.fetchall()

            diagnosticos = []
            for row in rows:
                id_diagnostico = row[0]
                UsuarioId = row[1]
                Edad = row[2]
                Peso = float(row[3])
                AlturaCM = float(row[4])
                Sexo = row[5]
                SeccionCuerpo = row[6]
                CondicionesPrevias = row[7]
                Imagen = row[8]

                diagnostico = {
                    "id_diagnostico": id_diagnostico,
                    "UsuarioId": UsuarioId,
                    "Edad": Edad,
                    "Peso": Peso,
                    "AlturaCM": AlturaCM,
                    "Sexo": Sexo,
                    "SeccionCuerpo": SeccionCuerpo,
                    "CondicionesPrevias": CondicionesPrevias,
                    "Imagen": Imagen
                }
                diagnosticos.append(diagnostico)

            connection.close()
            return diagnosticos

    except Exception as ex:
        raise ex
        return []
    

def eliminar_diagnostico(id_diagnostico):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Diagnostico WHERE id = %s;", (id_diagnostico,))
            connection.commit()
            connection.close()
            return True
    except Exception as ex:
        raise ex
        return False
