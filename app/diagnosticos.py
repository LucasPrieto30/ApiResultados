import base64
from flask_restx import Resource, Namespace, fields, api
import psycopg2
from .modelos import post_model, pacienteDiagnostico, post_model2, historial_parser, diag_parser
from .crud_diagnosticos import CrudDiagnostico
from flask import jsonify, request
from app.models.entities.Historial import Historial
from database.db import get_connection
from werkzeug.utils import secure_filename
import os
from psycopg2 import Binary
import requests
#random para prediccion res
import random

ns = Namespace("Pruebas")
ns2 = Namespace("Diagnosticos")
crud = CrudDiagnostico()

# archivos permitidos
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# recibe el nombre de un archivo y devuelve true si la extensión del archivo 
# está en el conjunto de extensiones permitidas y false en caso contrario.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ns.route("/imagen")
class Pruebas(Resource):
    @ns.expect(post_model)
    def post(self):
        return {"saludo": "hola post"}, 200
    
@ns.route("")
class Pruebas(Resource):
    def get(self):
        return {"saludo": "hola get"}, 200
    
@ns.route("/prediccion")
class PruebasPredicciones(Resource):
    def get(self):
        numeroPrediccion = round(random.uniform(0.00, 1.00), 2)
        if numeroPrediccion < 0.60:
            resultado = "No certero"
        elif 0.60 <= numeroPrediccion < 0.65:
            resultado = "Poco certero"
        else:
            resultado = "Muy certero"
        numeroPrediccionFormateado = '{:.2f}'.format(numeroPrediccion)
        print("el resultado ",numeroPrediccionFormateado,resultado)
        respuesta = {
            "precision": numeroPrediccionFormateado,
            "prediccion": resultado
        }
        return respuesta, 200
    
@ns.route('/historial/<int:id>')
class PruebaHistorial(Resource):
    def get(self,id):
        try:
           connection=get_connection()
           with connection.cursor() as cursor:
                cursor.execute(f'SELECT id, fecha, hora, estudio, descripcion FROM public."Historial" WHERE id=%s;',(id,))
                row = cursor.fetchone()
        
                if row != None:
                    historial= Historial(row[0], row[1], row[2], row[3], row[4])
                    connection.close()
                    
                    if historial != None:
                        return jsonify(historial.to_JSON())
                    return jsonify({"message": 'Historial no encontrado'})
                else: 
                    return jsonify({"message": 'Historial no encontrado'})       
        except Exception as ex:
            return jsonify({"message": str(ex)}),500
        
@ns2.route('/historial')
class HistorialResource(Resource):
    @ns.expect(historial_parser)
    def get(self):
        args = historial_parser.parse_args()

        id_usuario = args['id_usuario']
        rol_id = args['rol_id']

        try:
            connection=get_connection()
            with connection.cursor() as cursor:

                if rol_id == 4:
                    # Consulta para médicos
                    cursor.execute("SELECT * FROM public.diagnostico WHERE usuario_medico_id = %s", (id_usuario,))
                elif rol_id == 1:
                    # Consulta para auditores
                    cursor.execute("SELECT * FROM  public.diagnostico")
                else:
                    return {"error": "Rol no válido"}, 400

                historial = cursor.fetchall()
                cursor.close()
            
            # historial según la estructura del response
            historial_formateado = []
            for diagnostico in historial:
                historial_formateado.append({
                    "id": diagnostico[0],  
                    "imagen": base64.b64encode(diagnostico[1]).decode('utf-8'),
                    "datos_complementarios": diagnostico[2],
                    "fecha": diagnostico[3].strftime("%d-%m-%Y"),
                    "resultado": diagnostico[4],
                    "usuario_id": diagnostico[5],
                    "usuario_medico_id": diagnostico[6],
                    "modelo_id": diagnostico[7]
                })
            return {"historial": historial_formateado}
        
        except psycopg2.Error as e:
            return {"error": "Error al acceder a la base de datos"}, 500
        finally:
            connection.close()

@ns2.route('/predecir/cerebro')
class PruebaImagen(Resource):
    @ns.expect(diag_parser)
    def post(self):
        nuevo_diagnostico = diag_parser.parse_args()
        nuevo_diagnostico["debilidad_focal"] = request.values.get('debilidad_focal').lower() == 'true' 
        nuevo_diagnostico["convulsiones"] = request.values.get('convulsiones').lower() == 'true' 
        nuevo_diagnostico["perdida_visual"] = request.values.get('perdida_visual').lower() == 'true' 

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
            # URL de la API externa a la que deseas enviar la imagen
            url = f'https://averiapi-4vtuhnxfba-uc.a.run.app/predict/fred?perdida_visual={datos["perdida_visual"]}&debilidad_focal={datos["debilidad_focal"]}&convulsiones={datos["convulsiones"]}'
            
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
                return {'error': 'Error en la solicitud POST', 'status_code': response.status_code}, 500
        except Exception as ex:
            return {'message': "Error al obtener la predicción del modelo: " + str(ex)}, 500



@ns.route("/all")
class DiagnosticoListResource(Resource):
    @ns2.doc(responses={200: 'Éxito', 204: 'No hay diagnósticos para mostrar'})
    def get(self):
        diagnostico = crud.mostrar_diagnosticos()
        if diagnostico:
            return diagnostico, 200
        elif len(diagnostico) == 0:
            return {"message": "No hay diagnósticos disponibles para mostrar"}, 204

@ns2.route("/<int:id_diagnostico>")
class DiagnosticoResource(Resource):
    @ns2.doc(responses={200: 'Éxito', 204: 'No existe diagnostico con el id seleccionado'})
    def get(self, id_diagnostico):
        diagnostico = crud.obtener_diagnostico(id_diagnostico)
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
            cursor.execute("SELECT imagen FROM diagnostico WHERE id = %s", (diagnostico_id,))
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