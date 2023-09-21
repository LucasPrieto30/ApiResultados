from flask_restx import Resource, Namespace, fields
from .modelos import post_model

ns = Namespace("Pruebas")

@ns.route("/imagen")
class Pruebas(Resource):
    @ns.expect(post_model)
    def post(self):
        return {"saludo": "hola post"}, 200
    
@ns.route("/")
class Pruebas(Resource):
    def get(self):
        return {"saludo": "hola get"}, 200