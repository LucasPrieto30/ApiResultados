import base64
from flask_restx import Resource, Namespace, fields, api, reqparse
import psycopg2
from .modelos import post_model, pacienteDiagnostico, post_model2, historial_parser, diag_parser_cerebro, diag_parser_pulmones, diag_parser_corazon
from .crud_diagnosticos import CrudDiagnostico
from flask import jsonify, request
from app.models.entities.Historial import Historial
from database.db import get_connection
from database.dto_medico import verificar_Usuario_rol_medico
from werkzeug.utils import secure_filename
import os
from psycopg2 import Binary
import requests
#random para prediccion res
import random

ns = Namespace("Pruebas")
ns2 = Namespace("Diagnosticos")
feedbackNs = Namespace("Feedback")

crud = CrudDiagnostico()
parser = reqparse.RequestParser()
parser.add_argument('rol_id', required=True, help='Clave de acceso', location='args')  # 'args' indica que es un parámetro de consulta

# archivos permitidos
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# recibe el nombre de un archivo y devuelve true si la extensión del archivo 
# está en el conjunto de extensiones permitidas y false en caso contrario.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ns2.route('/historial')
class HistorialResource(Resource):
    @ns.expect(historial_parser)
    def get(self):
        args = historial_parser.parse_args()

        id_usuario = args['id_usuario']
        rol_id = args['rol_id']

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                query_sql = 'SELECT d.id, d.imagen_id, d.datos_complementarios, d.fecha, d.resultado, d.usuario_id, d.usuario_medico_dni, d.modelo_id, u.nombre as nombre_usuario, mo.nombre as modelo_nombre, me.nombre as nombre_medico, i.imagen as imagen FROM Diagnostico as d INNER JOIN public.usuario as u ON d.usuario_id = u.id INNER JOIN public.imagen_analisis as i ON d.imagen_id = i.imagen_id INNER JOIN public.modelo as mo ON mo.id = d.modelo_id LEFT JOIN public.usuario as me ON d.usuario_medico_dni = me.dni'

                if verificar_Usuario_rol_medico(rol_id):
                    cursor.execute(query_sql + " WHERE d.usuario_medico_id = %s", (id_usuario,))
                elif rol_id == 1:
                    # Consulta para auditores sin la columna "resultado"
                    #cursor.execute(query_sql)
                    cursor.execute(query_sql)

                else:
                    return {"error": "Rol no válido"}, 400

                historial = cursor.fetchall()
                cursor.close()
            
            # Historial formateado según la estructura del response
            historial_formateado = []
            for diagnostico in historial:
                diagnostico_dict = {
                    "id": diagnostico[0],
                    "imagen_id": diagnostico[1],
                    "datos_complementarios": diagnostico[2],
                    "fecha": diagnostico[3].strftime("%Y-%m-%d %H:%M:%S"),
                    "usuario_id": diagnostico[5],
                    "usuario_medico_dni": diagnostico[6],
                    "modelo_id": diagnostico[7],
                    "nombre_usuario": diagnostico[8],
                    "modelo_nombre": diagnostico[9],
                    "nombre_medico": diagnostico[10],
                    "imagen": base64.b64encode(base64.b64decode(diagnostico[11])).decode('utf-8')
                }

                # Verificar el rol y agregar o excluir la columna "resultado"
                if rol_id == 4 or rol_id == 1:
                    diagnostico_dict["resultado"] = diagnostico[4]

                historial_formateado.append(diagnostico_dict)

            return {"historial": historial_formateado}

        except psycopg2.Error as e:
            return {"error": "Error al acceder a la base de datos"}, 500
        finally:
            connection.close()

@ns2.route('/predecir/cerebro')
class PruebaImagen(Resource):
    @ns.expect(diag_parser_cerebro)
    def post(self):
        nuevo_diagnostico = diag_parser_cerebro.parse_args()
        nuevo_diagnostico["debilidad_focal"] = request.values.get('debilidad_focal').lower() == 'true' 
        nuevo_diagnostico["convulsiones"] = request.values.get('convulsiones').lower() == 'true' 
        nuevo_diagnostico["perdida_visual"] = request.values.get('perdida_visual').lower() == 'true' 
        nuevo_diagnostico["modelo_id"] = 1

        img = request.files['imagen']
       
        filename = ""
        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            img.save(os.path.join('app/static', filename))
        else:
            return {'msg': 'Solo se permiten cargar archivos png, jpg y jpeg'}

        datos = {
            'perdida_visual':nuevo_diagnostico['perdida_visual'],
            'debilidad_focal':nuevo_diagnostico['debilidad_focal'],
            'convulsiones': nuevo_diagnostico['convulsiones']
        }

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT (MAX(imagen_id) + 1) as siguiente_id FROM public.imagen_analisis;")
                siguiente_imagen_id = cursor.fetchone()[0]
                if (siguiente_imagen_id is None):
                    siguiente_imagen_id = 1
                nuevo_diagnostico["imagen_id"] = siguiente_imagen_id
                cursor.close()
                connection.close()
            # URL de la API externa a la que deseas enviar la imagen
            url = f'https://averiapi-4vtuhnxfba-uc.a.run.app/predict/fred?perdida_visual={datos["perdida_visual"]}&debilidad_focal={datos["debilidad_focal"]}&convulsiones={datos["convulsiones"]}&id_image={siguiente_imagen_id}'
            print(url)
            # Leer la imagen en formato binario
            with open(os.path.join('app/static', filename), 'rb') as file:
                image_data = file.read()
            
            # falta agregar datos complementarios a la request
            files = {'image': (filename, image_data, 'image/jpeg')}

            # Realizar la solicitud POST con los datos y la imagen
            response = requests.post(url, files=files) # data= datos
            print(response)
            # Procesar la respuesta
            if response.status_code == 200:
                # Si la respuesta es JSON, puedes cargarla como un diccionario
                data = response.json()
                # guarda el diagnostico cuando se obtiene el response
                crud.crear_diagnostico(nuevo_diagnostico, data, image_data)
                return data, 200
            else:
                return {'error': 'Error al obtener la predicción del modelo', 'status_code': response.status_code}, 500
        except Exception as ex:
            return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500
        
@ns2.route('/predecir/pulmones')
class PruebaImagen(Resource):
    @ns.expect(diag_parser_pulmones)
    def post(self):
        nuevo_diagnostico = diag_parser_pulmones.parse_args()
        nuevo_diagnostico["puntada_lateral"] = request.values.get('puntada_lateral').lower() == 'true' 
        nuevo_diagnostico["fiebre"] = request.values.get('fiebre').lower() == 'true' 
        nuevo_diagnostico["dificultad_respiratoria"] = request.values.get('dificultad_respiratoria').lower() == 'true' 
        nuevo_diagnostico["modelo_id"] = 2
        img = request.files['imagen']
       
        filename = ""
        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            img.save(os.path.join('app/static', filename))
        else:
            return {'msg': 'Solo se permiten cargar archivos png, jpg y jpeg'}

        datos = {
            'puntada_lateral':nuevo_diagnostico['puntada_lateral'],
            'fiebre':nuevo_diagnostico['fiebre'],
            'dificultad_respiratoria': nuevo_diagnostico['dificultad_respiratoria']
        }

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT (MAX(imagen_id) + 1) as siguiente_id FROM public.imagen_analisis;")
                siguiente_imagen_id = cursor.fetchone()[0]
                if (siguiente_imagen_id is None):
                    siguiente_imagen_id = 1
                nuevo_diagnostico["imagen_id"] = siguiente_imagen_id
                cursor.close()
                connection.close()
            # URL de la API externa a la que deseas enviar la imagen
            url = f'https://averiapi-4vtuhnxfba-uc.a.run.app/predict/wini?puntada_lateral={datos["puntada_lateral"]}&fiebre={datos["fiebre"]}&dificultad_respiratoria={datos["dificultad_respiratoria"]}&id_image={siguiente_imagen_id}'
            
            # Leer la imagen en formato binario
            with open(os.path.join('app/static', filename), 'rb') as file:
                image_data = file.read()
            
            # falta agregar datos complementarios a la request
            files = {'image': (filename, image_data, 'image/jpeg')}

            # Realizar la solicitud POST con los datos y la imagen
            response = requests.post(url, files=files) # data= datos

            # Procesar la respuesta
            if response.status_code == 200:
                # Si la respuesta es JSON, puedes cargarla como un diccionario
                data = response.json()
                # guarda el diagnostico cuando se obtiene el response
                crud.crear_diagnostico(nuevo_diagnostico, data, image_data)
                return data, 200
            else:
                return {'error': 'Error al obtener la predicción del modelo', 'status_code': response.status_code}, 500
        except Exception as ex:
            return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500
        
@ns2.route('/predecir/corazon')
class PruebaImagen(Resource):
    @ns.expect(diag_parser_corazon)
    def post(self):
        nuevo_diagnostico = diag_parser_corazon.parse_args()
        nuevo_diagnostico["modelo_id"] = 3             
        img = request.files['imagen']
       
        filename = ""
        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            img.save(os.path.join('app/static', filename))
        else:
            return {'msg': 'Solo se permiten cargar archivos png, jpg y jpeg'}
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT (MAX(imagen_id) + 1) as siguiente_id FROM public.imagen_analisis;")
            siguiente_imagen_id = cursor.fetchone()[0]
            if (siguiente_imagen_id is None):
                siguiente_imagen_id = 1
            nuevo_diagnostico["imagen_id"] = siguiente_imagen_id
        try:
            url = 'https://diagnosticaria-oe6mpxtbxa-uc.a.run.app/predict'
        
            with open(os.path.join('app/static', filename), 'rb') as file:
                image_data = file.read()
            
            files = {'file': (filename, image_data, 'image/jpeg')}

            response = requests.post(url, files=files) 
    
            if response.status_code == 200:
                data = response.json()
                # guarda el diagnostico cuando se obtiene el response
                crud.crear_diagnostico(nuevo_diagnostico, data, image_data)
                return data, 200
            else:
                return {'error': 'Error al obtener la predicción del modelo', 'status_code': response.status_code}, 500
        except Exception as ex:
            return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500

@ns2.route("/<int:id_diagnostico>")
class DiagnosticoResource(Resource):
    @ns2.expect(parser)
    @ns2.doc(responses={200: 'Éxito', 204: 'No existe diagnostico con el id seleccionado'})
    def get(self, id_diagnostico):
        args = parser.parse_args()
        rol = args['rol_id']
        print(rol)
        diagnostico = crud.obtener_diagnostico(id_diagnostico, rol)
        if diagnostico:
            return diagnostico, 200
        else:
            return {"message": "No existe diagnóstico con id" + str(id_diagnostico)}, 204

@ns2.route("/Delete/<int:id_diagnostico>")
class DiagnosticoDeleteResource(Resource):
    def delete(self,id_diagnostico):
        #diagnostico = crud.resetear_diagnosticos()
        if crud.eliminar_diagnostico(id_diagnostico):
            return {"message": "Diagnóstico eliminado correctamente"}, 200
        else:
            return {"error": "No se pudo eliminar el diagnóstico"}, 500
        

# extraer los datos binarios codificados en base64 
#datos_binarios_base64 = json_respuesta['imagen']

# decodificar los datos binarios base64
#datos_binarios = base64.b64decode(datos_binarios_base64)

# crear una imagen a partir de los datos binarios
#imagen = Image.open(io.BytesIO(datos_binarios))

# mostrar la imagen
#imagen.show()

from flask import send_file
import io 
from PIL import Image

@ns.route('/imagen/<int:diagnostico_id>')
class Imagen(Resource):
    def get(self, diagnostico_id):
        # Realizar una conexión a la base de datos
        connection = get_connection()
        cursor = connection.cursor()

        try:
            # Realizar una consulta para obtener la imagen
            cursor.execute("SELECT i.imagen FROM diagnostico d INNER JOIN public.imagen_analisis on d.imagen_id = i.imagen_id WHERE d.id = %s", (diagnostico_id,))
            imagen = cursor.fetchone()

            if imagen:
                # Obtener los datos de la imagen (de tipo bytea) desde la consulta
                datos_binarios_base64 = imagen[0]
                #imagen_bytes = imagen[0]
                #print(imagen_bytes)
                cadena_decodificada = base64.b64decode(datos_binarios_base64)

                if isinstance(cadena_decodificada, bytes):
                    print("esta en bytes")
                # Intenta abrir la imagen usando Pillow
                try:
                    image = Image.open(io.BytesIO(cadena_decodificada))

                    # Ahora puedes obtener el formato de la imagen
                    image_format = image.format.lower()  # Convierte a minúsculas para uniformidad

                    # Determina el mimetype basado en el formato de la imagen
                    if image_format == "jpeg":
                        mimetype = "image/jpeg"
                    elif image_format == "png":
                        mimetype = "image/png"
                    elif image_format == "gif":
                        mimetype = "image/gif"
                    # Agrega otros formatos si es necesario

                    # Devuelve la imagen con el mimetype correcto
                    return send_file(io.BytesIO(cadena_decodificada), mimetype=mimetype)
                except Exception as e:
        # Si no se puede abrir la imagen, maneja el error
                    return {"error": "Error al abrir la imagen: " + str(e)}, 500
            else:
                return {"message": "Imagen no encontrada"}, 404
        except Exception as e:
            return {"error": "Error al obtener la imagen: " + str(e)}, 500
        finally:
            cursor.close()
            connection.close()