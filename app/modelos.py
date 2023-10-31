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
diag_parser_cerebro.add_argument('dni_medico', type=str, required=True, help='DNI de médico')

# parametros para diagnostico del modelo: pulmones
diag_parser_pulmones = reqparse.RequestParser()
diag_parser_pulmones.add_argument('imagen', type=FileStorage, location='files', required=True, help='Imagen')
diag_parser_pulmones.add_argument('puntada_lateral', type=bool, required=True, help='puntada_lateral')
diag_parser_pulmones.add_argument('fiebre', type=bool, required=True, help='fiebre')
diag_parser_pulmones.add_argument('dificultad_respiratoria', type=bool, required=True, help='dificultad_respiratoria')
diag_parser_pulmones.add_argument('id_usuario', type=int, required=True, help='ID de usuario')
diag_parser_pulmones.add_argument('dni_medico', type=str, required=True, help='DNI de médico')


# parametros para diagnostico del modelo: corazon
diag_parser_corazon = reqparse.RequestParser()
diag_parser_corazon.add_argument('imagen', type=FileStorage, location='files', required=True, help='Imagen')
diag_parser_corazon.add_argument('id_usuario', type=int, required=True, help='ID de usuario')
diag_parser_corazon.add_argument('dni_medico', type=str, required=True, help='DNI de médico')

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



login_model = api.model('Login', {
    'dni': fields.String(required=True, description='DNI del usuario'),
    'password': fields.String(required=True, description='Contraseña del usuario'),
})

login_model_response = api.model('Usuario', {
    'id': fields.Integer(description='ID del usuario'),
    'nombre': fields.String(description='Nombre del usuario'),
    'rol_id': fields.Integer(description='ID del rol del usuario'),
    'dni': fields.String(description='DNI del usuario'),
    'email': fields.String(description='Correo electrónico del usuario'),
    'especialidad': fields.String(description='Especialidad del usuario'),
    'establecimiento_id': fields.String(description='establecimiento_id del usuario'),
})

verificar_codigo_model =  parser = reqparse.RequestParser()
parser.add_argument('codigo', type=str, required=True, help='Código OTP de 6 dígitos')

feedback_cerebro_args = reqparse.RequestParser()
feedback_cerebro_args.add_argument('imagen_id', type=int, required=True, help='Imagen id')
feedback_cerebro_args.add_argument('glioma', type=bool, required=False, help='glioma')
feedback_cerebro_args.add_argument('meningioma', type=bool, required=False, help='meningioma')
feedback_cerebro_args.add_argument('pituitary', type=bool, required=False, help='pituitary')
feedback_cerebro_args.add_argument('no_tumor', type=bool, required=False, help='no_tumor')

feedback_pulmones_args = reqparse.RequestParser()
feedback_pulmones_args.add_argument('imagen_id', type=int, required=True, help='Imagen id')
feedback_pulmones_args.add_argument('pneumonia', type=bool, required=False, help='pneumonia')
feedback_pulmones_args.add_argument('no_pneumonia', type=bool, required=False, help='no_pneumonia')
