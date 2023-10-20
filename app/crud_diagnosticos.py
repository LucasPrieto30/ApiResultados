import base64
import datetime
import json

import psycopg2
from database.dto_diagnostico import insert_diagnostico, obtener_diagnostico, obtener_todos_diagnosticos, eliminar_diagnostico
from psycopg2 import Binary

class CrudDiagnostico:
    def __init__(self):
        # Simulación de una lista de diagnósticos
        try:
            with open("diagnosticos.json", "r") as archivo_json:
                self.diagnosticos = json.load(archivo_json)
        except (FileNotFoundError, json.JSONDecodeError):
            self.diagnosticos = []

    # diagnostico modelo de cerebro
    def crear_diagnostico(self, datos_diagnostico, data, img_data):
        try:
            
            img_encoded = base64.b64encode(img_data).decode('utf-8')

            datos_complementarios = {
                'problemasVisuales': datos_diagnostico['problemasVisuales'],
                'decadenciaMotriz': datos_diagnostico['decadenciaMotriz'],
                'epilepsia': datos_diagnostico['epilepsia']
            }

            # Convertir el diccionario a formato JSON
            datos_complementarios_json = json.dumps(datos_complementarios)

            # Obtener la fecha actual
            fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # crear un diagnóstico con los datos
            nuevo_diagnostico = {
                "imagen": img_encoded,
                "datos_complementarios": datos_complementarios_json,
                "fecha": fecha_actual,
                "resultado": json.dumps(data), 
                "usuario_id":  datos_diagnostico['id_usuario'], 
                "id_medico": datos_diagnostico['id_medico'],
                "id_modelo": 1  
            }

            insert_diagnostico(nuevo_diagnostico)
        except Exception as ex:
                return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500
        
       
    def obtener_diagnostico(self, id_diagnostico):
        return obtener_diagnostico(id_diagnostico)
        
    ## si se pide a futuro
    def actualizar_diagnostico(self, id_diagnostico, nuevos_datos):
        # Lógica para actualizar un diagnóstico en la lista por su ID
        for diagnostico in self.diagnosticos:
            if diagnostico["id"] == id_diagnostico:
                diagnostico.update(nuevos_datos)
                #self.guardar_diagnosticos_en_json()

                return diagnostico
        return None
    ## si se pide a futuro
    def eliminar_diagnostico(self, id_diagnostico):
        # Lógica para eliminar un diagnóstico de la lista por su ID
        if eliminar_diagnostico(id_diagnostico):
            #self.guardar_diagnosticos_en_json()
            return True
        else:
            return False

    def mostrar_diagnosticos(self):
        lista_diagnosticos = []
        todos_diagnosticos = obtener_todos_diagnosticos()
        for diagnostico in todos_diagnosticos:
            datos_diagnostico = {
            "id": diagnostico["id_diagnostico"],
            "UsuarioId": diagnostico["UsuarioId"],
            "Id_rol": "null",  # Puedes adaptar este valor si es necesario
            "diagnostico/resultados": {
                "Edad": diagnostico["Edad"],
                "Peso": diagnostico["Peso"],
                "AlturaCM": diagnostico["AlturaCM"],
                "Sexo": diagnostico["Sexo"],
                "SeccionCuerpo": diagnostico["SeccionCuerpo"],
                "CondicionesPrevias": diagnostico["CondicionesPrevias"],
                "Imagen": diagnostico["Imagen"]
                }
            }
            lista_diagnosticos.append(datos_diagnostico)
        return lista_diagnosticos
    
##------metodos auxiliares--------##

    # Método para guardar la lista de diagnósticos en el archivo JSON
    def guardar_diagnosticos_en_json(self):
        with open("diagnosticos.json", "w") as archivo_json:
            json.dump(self.diagnosticos, archivo_json)

    def resetear_diagnosticos(self):
        self.diagnosticos = []  # Reiniciar la lista de diagnósticos
        self.guardar_diagnosticos_en_json()  # Guardar la lista vacía en el archivo JSON
        if len(self.diagnosticos) == 0:
            return True
        else:
            return False
        