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
diag_parser_cerebro = reqparse.RequestParser()
diag_parser_cerebro.add_argument('imagen', type=FileStorage, location='files', required=True, help='Imagen')
diag_parser_cerebro.add_argument('perdida_visual', type=bool, required=True, help='Pérdida visual')
diag_parser_cerebro.add_argument('debilidad_focal', type=bool, required=True, help='debilidad_focal')
diag_parser_cerebro.add_argument('convulsiones', type=bool, required=True, help='Convulsiones')
diag_parser_cerebro.add_argument('id_usuario', type=int, required=True, help='ID de usuario')
diag_parser_cerebro.add_argument('id_medico', type=int, required=True, help='ID de médico')

# parametros para diagnostico del modelo: pulmones
diag_parser_pulmones = reqparse.RequestParser()
diag_parser_pulmones.add_argument('imagen', type=FileStorage, location='files', required=True, help='Imagen')
diag_parser_pulmones.add_argument('puntada_lateral', type=bool, required=True, help='puntada_lateral')
diag_parser_pulmones.add_argument('fiebre', type=bool, required=True, help='fiebre')
diag_parser_pulmones.add_argument('dificultad_respiratoria', type=bool, required=True, help='dificultad_respiratoria')
diag_parser_pulmones.add_argument('id_usuario', type=int, required=True, help='ID de usuario')
diag_parser_pulmones.add_argument('id_medico', type=int, required=True, help='ID de médico')

from datetime import datetime

post_medico = api.model("PostMedico", {
    "nombre": fields.String(required=True),
    "dni": fields.String(required=True),  # Agrega el campo "dni" si es necesario
    "email": fields.String(attribute="email", required=True),
    "password": fields.String(required=True),
    "rol_id": fields.Integer(required=False),  # Agrega el campo "rol_id" si es necesario
    "establecimiento_id": fields.Integer(required=False),  # Agrega el campo "establecimiento_id" si es necesario
    "fecha_ultima_password": fields.DateTime(attribute="fecha_ultima_password", dt_format='iso8601'),
    "especialidad": fields.String(required=True)
})

