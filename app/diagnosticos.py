import base64
from flask_restx import Resource, Namespace, fields, api, reqparse
import psycopg2
from .modelos import post_model, pacienteDiagnostico, post_model2, historial_parser, diag_parser_cerebro, diag_parser_pulmones, diag_parser_corazon, feedback_cerebro_args, feedback_riñones_args, feedback_corazon_args, feedback_pulmones_args, feedback_rodilla_args, diag_parser_riñones,diag_parser_rodilla, feedback_muñeca_args, diag_parser_muñeca
from .crud_diagnosticos import CrudDiagnostico
from flask import jsonify, request
from database.db import get_connection
from database.dto_medico import verificar_Usuario_rol_medico
from werkzeug.utils import secure_filename
import os
from psycopg2 import Binary
import requests
#random para prediccion res
import random
from app.jwt_config import require_auth
import json
from database.dto_medico import obtener_clave_desde_Medico
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
def desencriptar_campo(campo, clave_maestra):
    if campo:
        # Comprueba si el campo es una cadena cifrada (generalmente una cadena base64)
        if isinstance(campo, str):
            # Intenta desencriptar el campo
            try:
                connection = get_connection()
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT pgp_sym_decrypt('{campo}'::bytea, %s, 'compress-algo=0,cipher-algo=AES128');", (clave_maestra,))
                    resultado = cursor.fetchone()
                connection.close()
                return resultado[0]
            except Exception as e:
                # No se pudo desencriptar el campo, así que se devuelve tal como está
                return campo
        else:
            # El campo no es una cadena cifrada, así que se devuelve tal como está
            return campo
    else:
        # El campo es None, se devuelve None
        return None

@ns2.route('/historial')
class HistorialResource(Resource):
    @ns2.doc(security=None)
    @ns2.doc(responses={200: 'Éxito', 400: 'Solicitud inválida', 500: 'Error interno del servidor'})
    @ns2.expect(historial_parser)
    def get(self):
        args = historial_parser.parse_args()

        id_usuario = args['id_usuario']
        rol_id = args['rol_id']
        clave_maestra=obtener_clave_desde_Medico()
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                query_sql = 'SELECT d.id, d.imagen_id, d.datos_complementarios, d.fecha, d.resultado, d.usuario_id, d.usuario_medico_dni, d.modelo_id, u.nombre as nombre_usuario, mo.nombre as modelo_nombre, me.nombre as nombre_medico, i.imagen as imagen, d.datos_paciente FROM Diagnostico as d INNER JOIN public.usuario as u ON d.usuario_id = u.id INNER JOIN public.imagen_analisis as i ON d.imagen_id = i.imagen_id INNER JOIN public.modelo as mo ON mo.id = d.modelo_id LEFT JOIN public.usuario as me ON d.usuario_medico_dni = me.dni'

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
                    "imagen": base64.b64encode(base64.b64decode(diagnostico[11])).decode('utf-8'),
                    "datos_paciente": desencriptar_campo(diagnostico[12], clave_maestra)
                }

                # Verificar el rol y agregar o excluir la columna "resultado"
                if rol_id == 4 or rol_id == 1:
                    diagnostico_dict["resultado"] = diagnostico[4]

                historial_formateado.append(diagnostico_dict)

            return {"historial": historial_formateado}

        except psycopg2.Error as e:
            #raise e
            return {"error": "Error al acceder a la base de datos"}, 500
        finally:
            connection.close()

@ns2.route('/predecir/cerebro')
class PruebaImagen(Resource):
    @ns2.doc(security=None)
    @ns2.doc(responses={200: 'Éxito', 500: 'Error al obtener la predicción del modelo', 400: 'Solicitud inválida'})
    @ns2.expect(diag_parser_cerebro)
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
            return {'msg': 'Solo se permiten cargar archivos png, jpg y jpeg'}, 400

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
                id_diagnostico = crud.crear_diagnostico(nuevo_diagnostico, data, image_data)
                data["id"] = id_diagnostico
                data["imagen_id"] = nuevo_diagnostico["imagen_id"]
                return data, 200
            else:
                return {'error': 'Error al obtener la predicción del modelo', 'status_code': response.status_code}, 500
        except Exception as ex:
            return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500
        
@ns2.route('/predecir/pulmones')
class PruebaImagen(Resource):
    @ns2.doc(security=None)
    @ns2.doc(responses={200: 'Éxito', 500: 'Error al obtener la predicción del modelo', 400: 'Solicitud inválida'})
    @ns2.expect(diag_parser_pulmones)
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
            return {'msg': 'Solo se permiten cargar archivos png, jpg y jpeg'}, 400

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
                id_diagnostico = crud.crear_diagnostico(nuevo_diagnostico, data, image_data)
                data["id"] = id_diagnostico
                data["imagen_id"] = nuevo_diagnostico["imagen_id"]
                return data, 200
            else:
                return {'error': 'Error al obtener la predicción del modelo', 'status_code': response.status_code}, 500
        except Exception as ex:
            return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500
        
@ns2.route('/predecir/corazon')
class PruebaImagen(Resource):
    @ns2.doc(security=None)
    @ns2.doc(responses={200: 'Éxito', 500: 'Error al obtener la predicción del modelo', 400: 'Solicitud inválida'})
    @ns2.expect(diag_parser_corazon)
    def post(self):
        nuevo_diagnostico = diag_parser_corazon.parse_args()
        nuevo_diagnostico["palpitaciones"] = request.values.get('palpitaciones') is not None and request.values.get('palpitaciones').lower()  == 'true' 
        nuevo_diagnostico["dolor_toracico_irradiado_a_cuello_mandíbula_miembro_superior_izquierdo"] = request.values.get('dolor_toracico_irradiado_a_cuello_mandíbula_miembro_superior_izquierdo') is not None and request.values.get('dolor_toracico_irradiado_a_cuello_mandíbula_miembro_superior_izquierdo').lower() == 'true' 
        nuevo_diagnostico["disnea"] = request.values.get('disnea') is not None and request.values.get('disnea').lower() == 'true' 
        nuevo_diagnostico["modelo_id"] = 3             
        img = request.files['imagen']
       
        filename = ""
        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            img.save(os.path.join('app/static', filename))
        else:
            return {'msg': 'Solo se permiten cargar archivos png, jpg y jpeg'}, 400
        
        datos = {
            'palpitaciones':nuevo_diagnostico['palpitaciones'],
            'dolor_tor_cm_msi':nuevo_diagnostico['dolor_toracico_irradiado_a_cuello_mandíbula_miembro_superior_izquierdo'],
            'disnea': nuevo_diagnostico['disnea']
        }

        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT (MAX(imagen_id) + 1) as siguiente_id FROM public.imagen_analisis;")
            siguiente_imagen_id = cursor.fetchone()[0]
            if (siguiente_imagen_id is None):
                siguiente_imagen_id = 1
            nuevo_diagnostico["imagen_id"] = siguiente_imagen_id
        try:
            datos_paciente = {
                'fecha_nacimiento': nuevo_diagnostico['fecha_nacimiento'],
                'peso': nuevo_diagnostico['peso'],
                'altura': nuevo_diagnostico['altura'],
                'sexo': nuevo_diagnostico['sexo'],
            }
            datos_paciente_json = json.dumps(datos_paciente)
            url = f'https://diagnosticaria-oe6mpxtbxa-uc.a.run.app/predict-egc' #?imagen_id={nuevo_diagnostico["imagen_id"]}&datos_paciente={datos_paciente_json}
        
            with open(os.path.join('app/static', filename), 'rb') as file:
                image_data = file.read()
            
            files = {'file': (filename, image_data, 'image/jpeg')}

            response = requests.post(url, files=files) 
    
            if response.status_code == 200:
                data = response.json()
                # guarda el diagnostico cuando se obtiene el response
                id_diagnostico = crud.crear_diagnostico(nuevo_diagnostico, data, image_data)
                data["id"] = id_diagnostico
                data["imagen_id"] = nuevo_diagnostico["imagen_id"]
                return data, 200
            else:
                return {'error': 'Error al obtener la predicción del modelo', 'status_code': response.status_code}, 500
        except Exception as ex:
            return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500

@ns2.route('/predecir/riñones')
class PruebaImagen(Resource):
    @ns2.doc(security=None) 
    @ns2.doc(responses={200: 'Éxito', 500: 'Error al obtener la predicción del modelo', 400: 'Solicitud inválida'})
    @ns2.expect(diag_parser_riñones)
    def post(self):
        nuevo_diagnostico = diag_parser_riñones.parse_args()
        nuevo_diagnostico["hermaturia"] = request.values.get('hermaturia').lower() == 'true' 
        nuevo_diagnostico["dolor_lumbar"] = request.values.get('dolor_lumbar').lower() == 'true' 
        nuevo_diagnostico["dolor_abdominal"] = request.values.get('dolor_abdominal').lower() == 'true' 
        nuevo_diagnostico["fiebre"] = request.values.get('fiebre').lower() == 'true' 
        nuevo_diagnostico["perdida_peso"] = request.values.get('perdida_peso').lower() == 'true' 
        nuevo_diagnostico["modelo_id"] = 4
        img = request.files['imagen']
       
        filename = ""
        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            img.save(os.path.join('app/static', filename))
        else:
            return {'msg': 'Solo se permiten cargar archivos jpg y jpeg'}, 400

        datos = {
            'hermaturia':nuevo_diagnostico['hermaturia'],
            'dolor_lumbar':nuevo_diagnostico['dolor_lumbar'],
            'dolor_abdominal':nuevo_diagnostico['dolor_abdominal'],
            'fiebre':nuevo_diagnostico['fiebre'],
            'perdida_peso': nuevo_diagnostico['perdida_peso']
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
            url = f'https://averiapi-4vtuhnxfba-uc.a.run.app/predict/lyso?hermaturia={datos["hermaturia"]}&dolor_lumbar={datos["dolor_lumbar"]}&dolor_abdominal={datos["dolor_abdominal"]}&fiebre={datos["fiebre"]}&perdida_peso={datos["perdida_peso"]}&id_image={siguiente_imagen_id}'
            
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
                id_diagnostico = crud.crear_diagnostico(nuevo_diagnostico, data, image_data)
                data["id"] = id_diagnostico
                data["imagen_id"] = nuevo_diagnostico["imagen_id"]
                return data, 200
            else:
                return {'error': 'Error al obtener la predicción del modelo', 'status_code': response.status_code}, 500
        except Exception as ex:
            return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500

@ns2.route('/predecir/rodilla')
class PruebaImagen(Resource):
    @ns2.doc(security=None)
    @ns2.doc(responses={200: 'Éxito', 500: 'Error al obtener la predicción del modelo', 400: 'Solicitud inválida'})
    @ns2.expect(diag_parser_rodilla)
    def post(self):
        nuevo_diagnostico = diag_parser_rodilla.parse_args()
        nuevo_diagnostico["sensacion_inestabilidad"] = request.values.get('sensacion_inestabilidad').lower() == 'true' 
        nuevo_diagnostico["CA_positiva"] = request.values.get('CA_positiva').lower() == 'true' 
        nuevo_diagnostico["impotencia_funcional"] = request.values.get('impotencia_funcional').lower() == 'true' 
        nuevo_diagnostico["modelo_id"] = 5

        archivo_zip = request.files['archivo'] 
        if not archivo_zip or archivo_zip.filename.endswith('.zip') == False: 
            return {'msg': 'Solo se permiten cargar archivos zip'}, 400 
 
        zip_data = archivo_zip.read()
       
        datos = {
            'sensacion_de_inestabilidad':nuevo_diagnostico['sensacion_inestabilidad'],
            'prueba_CA_positiva':nuevo_diagnostico['CA_positiva'],
            'impotencia_funcional':nuevo_diagnostico['impotencia_funcional']
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
            url = f'https://diagnosticaria-oe6mpxtbxa-uc.a.run.app/predict-lca'
           
            # falta agregar datos complementarios a la request
            files = {'file': ('archivo_zip', zip_data)}

            # Realizar la solicitud POST con los datos y la imagen
            response = requests.post(url, files=files) 
            
            # Procesar la respuesta
            if response.status_code == 200:
                # Si la respuesta es JSON, puedes cargarla como un diccionario
                image_data = response.json().get('image')
                data = response.json()
                data.pop('image', None)

                # guarda el diagnostico cuando se obtiene el response
                id_diagnostico = crud.crear_diagnostico(nuevo_diagnostico, data, image_data)
                data["id"] = id_diagnostico
                data["imagen_id"] = nuevo_diagnostico["imagen_id"]
                return data, 200
            else:
                return {'error': 'Error al obtener la predicción del modelo', 'status_code': response.status_code}, 500
        except Exception as ex:
            return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500

@ns2.route('/predecir/muñeca')
class PruebaImagen(Resource):
    @ns2.doc(security=None)
    @ns2.doc(responses={200: 'Éxito', 500: 'Error al obtener la predicción del modelo', 400: 'Solicitud inválida'})
    @ns2.expect(diag_parser_muñeca)
    def post(self):
        nuevo_diagnostico = diag_parser_muñeca.parse_args()
        nuevo_diagnostico["limitacion_funcional"] = request.values.get('limitacion_funcional').lower() == 'true' 
        nuevo_diagnostico["edema"] = request.values.get('edema').lower() == 'true' 
        nuevo_diagnostico["deformidad"] = request.values.get('deformidad').lower() == 'true' 
        nuevo_diagnostico["modelo_id"] = 6             
        img = request.files['imagen']
       
        filename = ""
        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            img.save(os.path.join('app/static', filename))
        else:
            return {'msg': 'Solo se permiten cargar archivos png, jpg y jpeg'}, 400
        
        datos = {
            'limitacion_funcional': nuevo_diagnostico['limitacion_funcional'],
            'edema': nuevo_diagnostico['edema'],
            'deformidad': nuevo_diagnostico['deformidad']
        }
        
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT (MAX(imagen_id) + 1) as siguiente_id FROM public.imagen_analisis;")
            siguiente_imagen_id = cursor.fetchone()[0]
            if (siguiente_imagen_id is None):
                siguiente_imagen_id = 1
            nuevo_diagnostico["imagen_id"] = siguiente_imagen_id
        try:
            datos_paciente = {
                'fecha_nacimiento': nuevo_diagnostico['fecha_nacimiento'],
                'peso': nuevo_diagnostico['peso'],
                'altura': nuevo_diagnostico['altura'],
                'sexo': nuevo_diagnostico['sexo'],
            }
            datos_paciente_json = json.dumps(datos_paciente)
            url = f'https://diagnosticaria-oe6mpxtbxa-uc.a.run.app/predict-fracture'   #imagen_id={nuevo_diagnostico["imagen_id"]}&datos_paciente={datos_paciente_json}
        
            with open(os.path.join('app/static', filename), 'rb') as file:
                image_data = file.read()
            
            files = {'file': (filename, image_data, 'image/jpeg')}

            response = requests.post(url, files=files) 
    
            if response.status_code == 200:
                data = response.json()
                # guarda el diagnostico cuando se obtiene el response
                id_diagnostico = crud.crear_diagnostico(nuevo_diagnostico, data, image_data)
                data["id"] = id_diagnostico
                data["imagen_id"] = nuevo_diagnostico["imagen_id"]
                return data, 200
            else:
                return {'error': 'Error al obtener la predicción del modelo', 'status_code': response.status_code}, 500
        except Exception as ex:
            return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500

@ns2.route("/<int:id_diagnostico>")
class DiagnosticoResource(Resource):
    @ns2.doc(security=None)
    @ns2.expect(parser)
    @ns2.doc(responses={200: 'Éxito', 404: 'No existe diagnostico con el id seleccionado'})
    def get(self, id_diagnostico):
        args = parser.parse_args()
        rol = args['rol_id']
        print(rol)
        diagnostico = crud.obtener_diagnostico(id_diagnostico, rol)
        if diagnostico:
            return diagnostico, 200
        else:
            return {"message": "No existe diagnóstico con id" + str(id_diagnostico)}, 404

@ns2.route("/Delete/<int:id_diagnostico>")
class DiagnosticoDeleteResource(Resource):
    @ns2.doc(security=None)
    @ns2.doc(responses={200: 'Diagnóstico eliminado correctamente', 500: 'No se pudo eliminar el diagnóstico'})
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
    @require_auth
    @ns.doc(responses={200: 'Éxito', 500: 'Error interno del servidor', 404: 'Imagen no encontrada'})
    def get(self,payload, diagnostico_id):
        # Realizar una conexión a la base de datos
        connection = get_connection()
        cursor = connection.cursor()

        try:
            # Realizar una consulta para obtener la imagen
            cursor.execute("SELECT i.imagen FROM public.diagnostico as d INNER JOIN public.imagen_analisis as i on d.imagen_id = i.imagen_id WHERE d.id = %s", (diagnostico_id,))
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

@feedbackNs.route('/cerebro')
class FeedbackCerebro(Resource):
    @feedbackNs.doc(security=None)
    @feedbackNs.expect(feedback_cerebro_args)
    @feedbackNs.doc(responses={200: 'Éxito', 404: 'Id de imagen no existente', 500: 'Server Error: Fallo al procesar la solicitud'})
    def post(self):
        feedback = feedback_cerebro_args.parse_args()
        feedback["glioma"] = request.values.get('glioma') is not None and request.values.get('glioma').lower() == 'true' 
        feedback["meningioma"] = request.values.get('meningioma') is not None and request.values.get('meningioma').lower() == 'true' 
        feedback["pituitary"] = request.values.get('pituitary') is not None and request.values.get('pituitary').lower() == 'true' 
        feedback["no_tumor"] = request.values.get('no_tumor') is not None and request.values.get('no_tumor').lower() == 'true' 
        feedback["imagen_id"] = request.values.get('imagen_id')
        try:
            url = f'https://averiapi-4vtuhnxfba-uc.a.run.app/feedback/fred?id_image={feedback["imagen_id"]}&glioma={feedback["glioma"]}&meningioma={feedback["meningioma"]}&pituitary={feedback["pituitary"]}&no_tumor={feedback["no_tumor"]}'
            if (request.values.get('comentario') is not None):
                url += "&comment="+request.values.get('comentario')
            response = requests.post(url) # data= datos
            # Procesar la respuesta
            if response.status_code == 200:
                data = response.json()
                return {"message": "Feedback enviado correctamente"}, 200
            elif response.status_code == 404:
                return {'error': 'Error al enviar el feedback del modelo: id de imagen no existente', 'status_code': response.status_code}, response.status_code
        except Exception as ex:
           return {'message': "Error al enviar el feedback al modelo: " + str(ex)}, 500

@feedbackNs.route('/pulmones')
class FeedbackPulmones(Resource):
    @feedbackNs.doc(security=None)
    @feedbackNs.expect(feedback_pulmones_args)
    @feedbackNs.doc(responses={200: 'Éxito', 404: 'Id de imagen no existente', 500: 'Server Error: Fallo al procesar la solicitud'})
    def post(self):
        feedback = feedback_pulmones_args.parse_args()
        feedback["pneumonia"] = request.values.get('pneumonia') is not None and request.values.get('pneumonia').lower() == 'true' 
        feedback["no_pneumonia"] = request.values.get('no_pneumonia') is not None and request.values.get('no_pneumonia').lower() == 'true' 
        feedback["imagen_id"] = request.values.get('imagen_id')
        print(feedback)
        try:
            url = f'https://averiapi-4vtuhnxfba-uc.a.run.app/feedback/wini?id_image={feedback["imagen_id"]}&pneumonia={feedback["pneumonia"]}&no_pneumonia={feedback["no_pneumonia"]}'
            if (request.values.get('comentario') is not None):
                url += "&comment="+request.values.get('comentario')
            print(url)
            response = requests.post(url)
            # Procesar la respuesta
            if response.status_code == 200:
                return {"message": "Feedback enviado correctamente"}, 200
            elif response.status_code == 404:
                return {'error': 'Error al enviar el feedback del modelo: id de imagen no existente', 'status_code': response.status_code}, response.status_code
        except Exception as ex:
           return {'message': "Error al enviar el feedback al modelo: " + str(ex)}, 500
        
@feedbackNs.route('/riñones')
class FeedbackRiñones(Resource):
    @feedbackNs.doc(security=None)
    @feedbackNs.expect(feedback_riñones_args)
    @feedbackNs.doc(responses={200: 'Éxito', 404: 'Id de imagen no existente', 500: 'Server Error: Fallo al procesar la solicitud'})
    def post(self):
        feedback = feedback_riñones_args.parse_args()
        feedback["quiste"] = request.values.get('quiste') is not None and request.values.get('quiste').lower() == 'true' 
        feedback["piedra"] = request.values.get('piedra') is not None and request.values.get('piedra').lower() == 'true' 
        feedback["tumor"] = request.values.get('tumor') is not None and request.values.get('tumor').lower() == 'true' 
        feedback["normal"] = request.values.get('normal') is not None and request.values.get('normal').lower() == 'true' 
        feedback["imagen_id"] = request.values.get('imagen_id')
        print(feedback)
        try:
            url = f'https://averiapi-4vtuhnxfba-uc.a.run.app/feedback/lyso?id_image={feedback["imagen_id"]}&quiste={feedback["quiste"]}&piedra={feedback["piedra"]}&tumor={feedback["tumor"]}&normal={feedback["normal"]}'
            if (request.values.get('comentario') is not None):
                url += "&comment="+request.values.get('comentario')
            print(url)
            response = requests.post(url)
            # Procesar la respuesta
            if response.status_code == 200:
                return {"message": "Feedback enviado correctamente"}, 200
            elif response.status_code == 404:
                return {'error': 'Error al enviar el feedback del modelo: id de imagen no existente', 'status_code': response.status_code}, response.status_code
        except Exception as ex:
           return {'message': "Error al enviar el feedback al modelo: " + str(ex)}, 500
        
@feedbackNs.route('/corazon')
class FeedbackCorazon(Resource):
    @feedbackNs.doc(security=None)
    @feedbackNs.expect(feedback_corazon_args)
    @feedbackNs.doc(responses={200: 'Éxito', 404: 'Id de imagen no existente', 500: 'Server Error: Fallo al procesar la solicitud'})
    def post(self):
        feedback = feedback_corazon_args.parse_args()
        feedback["contraccion_ventricular_prematura"] = request.values.get('contraccion_ventricular_prematura') is not None and request.values.get('contraccion_ventricular_prematura').lower() == 'true' 
        feedback["fusion_de_latido_ventricular_y_normal"] = request.values.get('fusion_de_latido_ventricular_y_normal') is not None and request.values.get('fusion_de_latido_ventricular_y_normal').lower() == 'true' 
        feedback["infarto_de_miocardio"] = request.values.get('infarto_de_miocardio') is not None and request.values.get('infarto_de_miocardio').lower() == 'true' 
        feedback["latido_no_clasificable"] = request.values.get('latido_no_clasificable') is not None and request.values.get('latido_no_clasificable').lower() == 'true' 
        feedback["latido_normal"] = request.values.get('latido_normal') is not None and request.values.get('latido_normal').lower() == 'true' 
        feedback["latido_prematuro_supraventricular"] = request.values.get('latido_prematuro_supraventricular') is not None and request.values.get('latido_prematuro_supraventricular').lower() == 'true' 
        feedback["imagen_id"] = request.values.get('imagen_id')
        print(feedback)
        try:
            url = f'https://diagnosticaria-oe6mpxtbxa-uc.a.run.app------?id_image={feedback["imagen_id"]}&contraccion_ventricular_prematura={feedback["contraccion_ventricular_prematura"]}&fusion_de_latido_ventricular_y_normal={feedback["fusion_de_latido_ventricular_y_normal"]}&infarto_de_miocardio={feedback["infarto_de_miocardio"]}&latido_no_clasificable={feedback["latido_no_clasificable"]}&latido_normal={feedback["latido_normal"]}&latido_prematuro_supraventricular={feedback["latido_prematuro_supraventricular"]}'
            if (request.values.get('comentario') is not None):
                url += "&comentario="+request.values.get('comentario')
            print(url)
            response = requests.post(url)
            # Procesar la respuesta
            if response.status_code == 200:
                return {"message": "Feedback enviado correctamente"}, 200
            elif response.status_code == 404:
                return {'error': 'Error al enviar el feedback del modelo: id de imagen no existente', 'status_code': response.status_code}, response.status_code
        except Exception as ex:
           return {'message': "Error al enviar el feedback al modelo: " + str(ex)}, 500
        
@feedbackNs.route('/rodilla')
class FeedbackRodilla(Resource):
    @feedbackNs.doc(security=None)
    @feedbackNs.expect(feedback_rodilla_args)
    @feedbackNs.doc(responses={200: 'Éxito', 404: 'Id de imagen no existente', 500: 'Server Error: Fallo al procesar la solicitud'})
    def post(self):
        feedback = feedback_rodilla_args.parse_args()
        feedback["rotura_lca"] = request.values.get('rotura_lca') is not None and request.values.get('rotura_lca').lower() == 'true' 
        feedback["lca_sano"] = request.values.get('lca_sano') is not None and request.values.get('lca_sano').lower() == 'true' 
        feedback["imagen_id"] = request.values.get('imagen_id')
        print(feedback)
        try:
            url = f'https://diagnosticaria-oe6mpxtbxa-uc.a.run.app------?id_image={feedback["imagen_id"]}&rotura_lca={feedback["rotura_lca"]}&lca_sano={feedback["lca_sano"]}'
            if (request.values.get('comentario') is not None):
                url += "&comentario="+request.values.get('comentario')
            print(url)
            response = requests.post(url)
            # Procesar la respuesta
            if response.status_code == 200:
                return {"message": "Feedback enviado correctamente"}, 200
            elif response.status_code == 404:
                return {'error': 'Error al enviar el feedback del modelo: id de imagen no existente', 'status_code': response.status_code}, response.status_code
        except Exception as ex:
           return {'message': "Error al enviar el feedback al modelo: " + str(ex)}, 500
        
@feedbackNs.route('/muñeca')
class FeedbackMuñeca(Resource):
    @feedbackNs.doc(security=None)
    @feedbackNs.expect(feedback_muñeca_args)
    @feedbackNs.doc(responses={200: 'Éxito', 404: 'Id de imagen no existente', 500: 'Server Error: Fallo al procesar la solicitud'})
    def post(self):
        feedback = feedback_muñeca_args.parse_args()
        feedback["fractura"] = request.values.get('fractura') is not None and request.values.get('fractura').lower() == 'true' 
        feedback["sin_fractura"] = request.values.get('sin_fractura') is not None and request.values.get('sin_fractura').lower() == 'true' 
        feedback["imagen_id"] = request.values.get('imagen_id')
        print(feedback)
        try:
            #corregir la url cuando este hecho el endpoint del equipo 2
            url = f'https://diagnosticaria-oe6mpxtbxa-uc.a.run.app------?id_image={feedback["imagen_id"]}&fractura={feedback["fractura"]}&sin_fractura={feedback["sin_fractura"]}'
            if (request.values.get('comentario') is not None):
                url += "&comentario="+request.values.get('comentario')
            print(url)
            response = requests.post(url)
            # Procesar la respuesta
            if response.status_code == 200:
                return {"message": "Feedback enviado correctamente"}, 200
            elif response.status_code == 404:
                return {'error': 'Error al enviar el feedback del modelo: id de imagen no existente', 'status_code': response.status_code}, response.status_code
        except Exception as ex:
           return {'message': "Error al enviar el feedback al modelo: " + str(ex)}, 500