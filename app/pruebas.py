from flask_restx import Resource, Namespace, fields
from .modelos import post_model, post_model1
from .crud_diagnosticos import CrudDiagnostico
#random para prediccion res
import random

ns = Namespace("Pruebas")
ns2 = Namespace("Pruebas de Diagnosticos")
crud = CrudDiagnostico()


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
    


@ns2.route("/Diagnóstico_GET")
class DiagnosticoListResource(Resource):
    def get(self):
        diagnostico = crud.mostrar_diagnosticos()
        if diagnostico:
            return diagnostico, 200
        else:
            return {"error": "Diagnósticos no encontrado o lista vacia"}, 404

@ns2.route("/Diagnóstico_GET_ID/<int:id_diagnostico>")
class DiagnosticoResource(Resource):
    def get(self, id_diagnostico):
        diagnostico = crud.obtener_diagnostico(id_diagnostico)
        if diagnostico:
            return diagnostico, 200
        else:
            return {"error": "Diagnóstico no encontrado o id no existe"}, 404

@ns2.route("/Diagnóstico_POST")
class DiagnosticoCreate(Resource):
    @ns.expect(post_model1)
    def post(self):
        # tener los datos del diagnóstico del cuerpo de la solicitud
        nuevo_diagnostico = ns.payload

        # Llama al método para crear un diagnóstico en el CRUD
        resultado = crud.crear_diagnostico(nuevo_diagnostico)

        if resultado:
            return resultado, 201  # Devuelve el diagnóstico creado y el código 201 (Created)
        else:
            return {"error": "No se pudo crear el diagnóstico"}, 500  # En caso de error



@ns2.route("/Diagnóstico_delete_ejemplo")
class DiagnosticoDeleteResource(Resource):
    def delete(self):
        #diagnostico = crud.resetear_diagnosticos()
        if crud.resetear_diagnosticos():
            return {"message": "Diagnósticos eliminados correctamente"}, 200
        else:
            return {"error": "Diagnósticos no se pudo borrar"}, 404