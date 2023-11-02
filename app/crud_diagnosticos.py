import base64
import datetime
import json
import pytz
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
            if(datos_diagnostico['modelo_id'] == 5):
                img_encoded = img_data
            else:
                img_encoded = base64.b64encode(img_data).decode('utf-8')
            datos_complementarios = {}
          
            if(datos_diagnostico['modelo_id'] == 1):
                datos_complementarios = {
                    'perdida_visual': datos_diagnostico['perdida_visual'],
                    'debilidad_focal': datos_diagnostico['debilidad_focal'],
                    'convulsiones': datos_diagnostico['convulsiones']
                }
            elif(datos_diagnostico['modelo_id'] == 2):
                datos_complementarios = {
                    'puntada_lateral': datos_diagnostico['puntada_lateral'],
                    'fiebre': datos_diagnostico['fiebre'],
                    'dificultad_respiratoria': datos_diagnostico['dificultad_respiratoria']
                }
            elif(datos_diagnostico['modelo_id'] == 3):
                datos_complementarios = {}
            elif(datos_diagnostico['modelo_id'] == 4):
                datos_complementarios = {
                    'hermaturia': datos_diagnostico['hermaturia'],
                    'dolor_lumbar':datos_diagnostico['dolor_lumbar'],
                    'dolor_abdominal':datos_diagnostico['dolor_abdominal'],
                    'fiebre':datos_diagnostico['fiebre'],
                    'perdida_peso': datos_diagnostico['perdida_peso']
                }
            elif(datos_diagnostico['modelo_id'] == 5):
                datos_complementarios = {
                    'sensacion_de_inestabilidad':datos_diagnostico['sensacion_inestabilidad'],
                    'prueba_CA_positiva':datos_diagnostico['CA_positiva'],
                    'impotencia_funcional':datos_diagnostico['impotencia_funcional']
                }

            datos_paciente = {
                'fecha_nacimiento': datos_diagnostico['fecha_nacimiento'],
                'peso': datos_diagnostico['peso'],
                'altura': datos_diagnostico['altura'],
                'sexo': datos_diagnostico['sexo'],
            }

            datos_paciente_json = json.dumps(datos_paciente)
            # Convertir el diccionario a formato JSON
            datos_complementarios_json = json.dumps(datos_complementarios)
            # Define la zona horaria de Argentina
            zona_horaria_argentina = pytz.timezone('America/Argentina/Buenos_Aires')

            # Obtiene la fecha y hora actual en la zona horaria de Argentina
            fecha_hora_argentina = datetime.datetime.now(zona_horaria_argentina)
            # Obtener la fecha actual
            fecha_actual = fecha_hora_argentina.strftime('%Y-%m-%d %H:%M:%S')
            # crear un diagnóstico con los datos
            nuevo_diagnostico = {
                "imagen": img_encoded,
                "imagen_id": datos_diagnostico['imagen_id'],
                "datos_complementarios": datos_complementarios_json,
                "fecha": fecha_actual,
                "resultado": json.dumps(data), 
                "usuario_id":  datos_diagnostico['id_usuario'], 
                "dni_medico": datos_diagnostico['dni_medico'],
                "id_modelo": datos_diagnostico['modelo_id'],
                "datos_paciente": datos_paciente_json
            }
            
            id_diagnostico = insert_diagnostico(nuevo_diagnostico)
            return id_diagnostico
        except Exception as ex:
                return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500
        
       
    def obtener_diagnostico(self, id_diagnostico,rol):
        return obtener_diagnostico(id_diagnostico,rol)
        
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
        