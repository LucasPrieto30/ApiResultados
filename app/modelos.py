from flask_restx import fields, reqparse
from .extensions import api
from werkzeug.datastructures import FileStorage

post_model = api.model("PostImagen", {
    "img": fields.String
})
pacienteDiagnostico = api.model("pacienteDiagnostico", {
    "UsuarioId": fields.String,
    "Edad": fields.Integer,
    "Peso": fields.Float,
    "AlturaCM": fields.Float,
    "Sexo": fields.String,
    "SeccionCuerpo": fields.String,
    "CondicionesPrevias": fields.String,
    "Imagen": fields.String
})

# argumentos para solicitud post, key= img, tipo=file
post_model2 = api.parser().add_argument('img', location='files', type='file')

# parametros para solicitar un historial
historial_parser = reqparse.RequestParser()
historial_parser.add_argument('id_usuario', type=int, required=True, help='ID de usuario')
historial_parser.add_argument('rol_id', type=int, required=True, help='Rol ID')

# parametros para diagnostico del modelo: cerebro
diag_parser = reqparse.RequestParser()
diag_parser.add_argument('imagen', type=FileStorage, location='files', required=True, help='Imagen')
diag_parser.add_argument('problemasVisuales', type=bool, required=True, help='Problemas visuales')
diag_parser.add_argument('decadenciaMotriz', type=bool, required=True, help='Decadencia motriz')
diag_parser.add_argument('epilepsia', type=bool, required=True, help='Epilepsia')
diag_parser.add_argument('id_usuario', type=int, required=True, help='ID de usuario')
diag_parser.add_argument('id_medico', type=int, required=True, help='ID de médico')
