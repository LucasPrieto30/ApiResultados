from flask_restx import Resource, Namespace, fields
from .modelos import post_model, pacienteDiagnostico
from .crud_diagnosticos import CrudDiagnostico
#random para prediccion res
import random

ns = Namespace("Pruebas")
ns2 = Namespace("Diagnosticos")
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



@ns2.route("/deleteAll")
class DiagnosticoDeleteResource(Resource):
    def delete(self):
        #diagnostico = crud.resetear_diagnosticos()
        if crud.resetear_diagnosticos():
            return {"message": "Diagnósticos eliminados correctamente"}, 200
        else:
            return {"error": "No se pudieron eliminar los diagnósticos"}, 500