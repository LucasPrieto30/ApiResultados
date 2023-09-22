from flask_restx import Resource, Namespace, fields
from .modelos import post_model
from flask_cors import cross_origin

ns = Namespace("Pruebas")

@ns.route("/imagen")

class Pruebas(Resource):
    @ns.expect(post_model)
    @cross_origin()
    def post(self):
        return {"saludo": "hola post"}, 200
    
@ns.route("/")
@cross_origin()
class Pruebas(Resource):
    @cross_origin()
    def get(self):
        return {"saludo": "hola get"}, 200