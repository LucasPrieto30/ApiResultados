
from database.db import get_connection
from psycopg2.extras import RealDictCursor


def insert_diagnostico(datos_diagnostico):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        insert_query = """
        INSERT INTO Diagnostico (UsuarioId, Edad, Peso, AlturaCM, Sexo, SeccionCuerpo, CondicionesPrevias, Imagen)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            datos_diagnostico.get("UsuarioId"),
            int(datos_diagnostico.get("Edad")),
            float(datos_diagnostico.get("Peso")),
            float(datos_diagnostico.get("AlturaCM")),
            datos_diagnostico.get("Sexo"),
            datos_diagnostico.get("SeccionCuerpo"),
            datos_diagnostico.get("CondicionesPrevias"),
            datos_diagnostico.get("Imagen")
        ))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        raise e
        return False
    finally:
        cursor.close()
        connection.close()

def obtener_diagnostico(id_diagnostico):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT id_diagnostico, UsuarioId, Edad, Peso, AlturaCM, Sexo, SeccionCuerpo, CondicionesPrevias, Imagen FROM Diagnostico WHERE id_diagnostico=%s;', (id_diagnostico,))
            row = cursor.fetchone()

            if row is not None:
                Peso_decimal = row[3]
                AlturaCM_decimal = row[4]
                Peso_float = float(Peso_decimal)
                AlturaCM_float = float(AlturaCM_decimal)

                diagnostico = {
                    "id_diagnostico": row[0],
                    "UsuarioId": row[1],
                    "Edad": row[2],
                    "Peso": Peso_float,
                    "AlturaCM": AlturaCM_float,
                    "Sexo": row[5],
                    "SeccionCuerpo": row[6],
                    "CondicionesPrevias": row[7],
                    "Imagen": row[8]
                }
                connection.close()
            
                if diagnostico is not None:
                    return diagnostico
                return None
            else:
                return None
    except Exception as ex:
        raise ex
        return None

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
            cursor.execute("DELETE FROM Diagnostico WHERE id_diagnostico = %s;", (id_diagnostico,))
            connection.commit()
            connection.close()
            return True
    except Exception as ex:
        raise ex
        return False
