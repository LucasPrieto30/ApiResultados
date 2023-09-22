from flask_restx import Resource, Namespace, fields
from .modelos import post_model
from flask_cors import CORS

ns = Namespace("Pruebas")

@ns.route("/imagen")
@cross_origin()
class Pruebas(Resource):
    @ns.expect(post_model)
    def post(self):
        return {"saludo": "hola post"}, 200
    
@ns.route("/")
@cross_origin()
class Pruebas(Resource):
    def get(self):
        return {"saludo": "hola get"}, 200