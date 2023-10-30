
import base64
from database.db import get_connection
from psycopg2.extras import RealDictCursor

# insertar diagnostico de modelo: cerebro
def insert_diagnostico(datos_diagnostico):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM usuario WHERE dni = %s", (datos_diagnostico.get("dni_medico"),))
            medicoExiste = cursor.fetchone()
            
            insert_query = """
            INSERT INTO public.diagnostico(imagen_id, datos_complementarios, fecha, resultado, usuario_id, modelo_id, usuario_medico_dni, usuario_medico_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
            )
            cursor.execute("INSERT INTO public.imagen_analisis (imagen_id, imagen) VALUES (%s, %s);", (datos_diagnostico.get("imagen_id"), datos_diagnostico.get("imagen")))
            cursor.execute(insert_query, values)
            connection.commit()
    except Exception as e:
        connection.rollback()
        return {'error': str(e)}

def obtener_diagnostico(id_diagnostico, rol):
    diagnostico = None

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT d.id, d.imagen_id, d.datos_complementarios, d.fecha, d.resultado, d.usuario_id, d.usuario_medico_dni, d.modelo_id, u.nombre as nombre_usuario, mo.nombre as modelo_nombre, me.nombre as nombre_medico, i.imagen as imagen FROM Diagnostico as d INNER JOIN public.usuario as u ON d.usuario_id = u.id INNER JOIN public.imagen_analisis as i ON d.imagen_id = i.imagen_id INNER JOIN public.modelo as mo ON mo.id = d.modelo_id LEFT JOIN public.usuario as me ON d.usuario_medico_dni = me.dni WHERE d.id=%s;', (id_diagnostico,))
            
            row = cursor.fetchone()
            if(row is None):
                return None
            imagen_decodificada =  base64.b64decode(row[11])
            imagen_base64 = base64.b64encode(imagen_decodificada).decode('utf-8')

            if row is not None:
                diagnostico = {
                    "id": row[0],  
                    "imagen_id": row[1],
                    "datos_complementarios": row[2],
                    "fecha": row[3].strftime("%Y-%m-%d %H:%M:%S"),
                    #"resultado": row[4],
                    "usuario_id": row[5],
                    "usuario_medico_dni": row[6],
                    "modelo_id": row[7],
                    "nombre_usuario": row[8],
                    "modelo_nombre": row[9],
                    "nombre_medico": row[10],
                    "imagen": imagen_base64,
                }
                if int(rol) == 4 or int(rol) == 1:
                    diagnostico["resultado"] = row[4]

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
