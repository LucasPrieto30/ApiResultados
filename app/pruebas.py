from flask_restx import Resource, Namespace, fields
from .modelos import post_model, pacienteDiagnostico, post_model2
from .crud_diagnosticos import CrudDiagnostico
from flask import jsonify, request
from app.models.entities.Historial import Historial
from database.db import get_connection
from werkzeug.utils import secure_filename
import os
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
    
@ns.route("/predicciones")
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
        
@ns.route('/cargar-imagen')
class PruebaImagen(Resource):
    @ns.expect(post_model2)
    def post(self):
        try:
            if 'img' not in request.files:
                return {'error': 'No se adjuntó ningún archivo'}, 400
            
            img = request.files['img']
            if allowed_file(img.filename):
                filename = secure_filename(img.filename)
                img.save(os.path.join('app/static', filename)) # la imagen se guarda en la carpeta 'static'
                return {'message': 'Imagen cargada exitosamente'}
            else:
                return {'msg': 'Solo se permiten cargar archivos png, jpg y jpeg'}
        except Exception as ex:
            return {'message': str(ex)}, 500


@ns2.route("/all")
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

@ns2.route("")
class DiagnosticoCreate(Resource):
    @ns.expect(pacienteDiagnostico)
    @ns2.doc(responses={201: 'Éxito', 500: 'Error al enviar el diagnóstico'})
    def post(self):
        # tener los datos del diagnóstico del cuerpo de la solicitud
        nuevo_diagnostico = ns.payload

        # Llama al método para crear un diagnóstico en el CRUD
        resultado = crud.crear_diagnostico(nuevo_diagnostico)

        if resultado:
            return resultado, 201  # Devuelve el diagnóstico creado y el código 201 (Created)
        else:
            return {"error": "No se pudo crear el diagnóstico"}, 500  # En caso de error



@ns2.route("/Delete/<int:id_diagnostico>")
class DiagnosticoDeleteResource(Resource):
    def delete(self,id_diagnostico):
        #diagnostico = crud.resetear_diagnosticos()
        if crud.eliminar_diagnostico(id_diagnostico):
            return {"message": "Diagnóstico eliminado correctamente"}, 200
        else:
            return {"error": "No se pudo eliminar el diagnóstico"}, 500
        