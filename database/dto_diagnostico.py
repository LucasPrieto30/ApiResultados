
import base64
from database.db import get_connection
from psycopg2.extras import RealDictCursor

# insertar diagnostico de modelo: cerebro
def insert_diagnostico(datos_diagnostico):
    try:
        connection=get_connection()
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO public.diagnostico(imagen, datos_complementarios, fecha, resultado, usuario_id, usuario_medico_id, modelo_id)
            VALUES ( %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                datos_diagnostico.get("imagen"),
                datos_diagnostico.get("datos_complementarios"),
                datos_diagnostico.get("fecha"),
                datos_diagnostico.get("resultado"),
                datos_diagnostico.get("usuario_id"),
                datos_diagnostico.get("id_medico"),
                datos_diagnostico.get("id_modelo"),
            ))
            connection.commit()
    except Exception as e:
        connection.rollback()
        return {'error': str(e)}

def obtener_diagnostico(id_diagnostico):
    diagnostico = None

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT d.id, d.imagen, d.datos_complementarios, d.fecha, d.resultado, d.usuario_id, d.usuario_medico_id, d.modelo_id, u.nombre as nombre_usuario, mo.nombre as modelo_nombre, me.nombre as nombre_medico FROM Diagnostico as d INNER JOIN public.usuario as u ON d.usuario_id = u.id INNER JOIN public.modelo as mo ON mo.id = d.modelo_id LEFT JOIN public.usuario as me ON d.usuario_medico_id = me.id WHERE d.id=%s;', (id_diagnostico,))
            row = cursor.fetchone()

            if row is not None:
                diagnostico = {
                    "id": row[0],  
                    "imagen": base64.b64encode(row[1]).decode('utf-8'),
                    "datos_complementarios": row[2],
                    "fecha": row[3].strftime("%d-%m-%Y"),
                    "resultado": row[4],
                    "usuario_id": row[5],
                    "usuario_medico_id": row[6],
                    "modelo_id": row[7],
                    "nombre_usuario": row[8],
                    "modelo_nombre": row[9],
                    "nombre_medico": row[10],
                }
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
