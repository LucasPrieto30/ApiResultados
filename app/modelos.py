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
diag_parser_cerebro.add_argument('fecha_nacimiento', type=str, required=True, help='Fecha de nacimiento del paciente')
diag_parser_cerebro.add_argument('peso', type=int, required=True, help='Peso del pacietnte en KG')
diag_parser_cerebro.add_argument('altura', type=int, required=True, help='Altura del paciente en CM')
diag_parser_cerebro.add_argument('sexo', type=str, required=True, help='Sexo del paciente')

# parametros para diagnostico del modelo: pulmones
diag_parser_pulmones = reqparse.RequestParser()
diag_parser_pulmones.add_argument('imagen', type=FileStorage, location='files', required=True, help='Imagen')
diag_parser_pulmones.add_argument('puntada_lateral', type=bool, required=True, help='puntada_lateral')
diag_parser_pulmones.add_argument('fiebre', type=bool, required=True, help='fiebre')
diag_parser_pulmones.add_argument('dificultad_respiratoria', type=bool, required=True, help='dificultad_respiratoria')
diag_parser_pulmones.add_argument('id_usuario', type=int, required=True, help='ID de usuario')
diag_parser_pulmones.add_argument('dni_medico', type=str, required=True, help='DNI de médico')
diag_parser_pulmones.add_argument('fecha_nacimiento', type=str, required=True, help='Fecha de nacimiento del paciente')
diag_parser_pulmones.add_argument('peso', type=int, required=True, help='Peso del pacietnte en KG')
diag_parser_pulmones.add_argument('altura', type=int, required=True, help='Altura del paciente en CM')
diag_parser_pulmones.add_argument('sexo', type=str, required=True, help='Sexo del paciente')

# parametros para diagnostico del modelo: corazon
diag_parser_corazon = reqparse.RequestParser()
diag_parser_corazon.add_argument('imagen', type=FileStorage, location='files', required=True, help='Imagen')

diag_parser_corazon.add_argument('palpitaciones', type=bool, required=False, help='palpitaciones')
diag_parser_corazon.add_argument('dolor_toracico_irradiado_a_cuello_mandíbula_miembro_superior_izquierdo', type=bool, required=False, help='Dolor torácico o irradiado a cuello, mandíbula y miembro superior izquierdo')
diag_parser_corazon.add_argument('disnea', type=bool, required=False, help='Disnea')

diag_parser_corazon.add_argument('id_usuario', type=int, required=True, help='ID de usuario')
diag_parser_corazon.add_argument('dni_medico', type=str, required=True, help='DNI de médico')
diag_parser_corazon.add_argument('fecha_nacimiento', type=str, required=True, help='Fecha de nacimiento del paciente')
diag_parser_corazon.add_argument('peso', type=int, required=True, help='Peso del pacietnte en KG')
diag_parser_corazon.add_argument('altura', type=int, required=True, help='Altura del paciente en CM')
diag_parser_corazon.add_argument('sexo', type=str, required=True, help='Sexo del paciente')

# parametros para diagnostico del modelo: riñones
diag_parser_riñones = reqparse.RequestParser()
diag_parser_riñones.add_argument('imagen', type=FileStorage, location='files', required=True, help='Imagen')
diag_parser_riñones.add_argument('hermaturia', type=bool, required=True, help='hematuria')
diag_parser_riñones.add_argument('dolor_lumbar', type=bool, required=True, help='dolor_lumbar')
diag_parser_riñones.add_argument('dolor_abdominal', type=bool, required=True, help='dolor_abdominal')
diag_parser_riñones.add_argument('fiebre', type=bool, required=True, help='fiebre')
diag_parser_riñones.add_argument('perdida_peso', type=bool, required=True, help='perdida_peso')
diag_parser_riñones.add_argument('id_usuario', type=int, required=True, help='ID de usuario')
diag_parser_riñones.add_argument('dni_medico', type=str, required=True, help='DNI de médico')
diag_parser_riñones.add_argument('fecha_nacimiento', type=str, required=True, help='Fecha de nacimiento del paciente')
diag_parser_riñones.add_argument('peso', type=int, required=True, help='Peso del pacietnte en KG')
diag_parser_riñones.add_argument('altura', type=int, required=True, help='Altura del paciente en CM')
diag_parser_riñones.add_argument('sexo', type=str, required=True, help='Sexo del paciente')

# parametros para diagnostico del modelo: rodilla
diag_parser_rodilla = reqparse.RequestParser()
diag_parser_rodilla.add_argument('archivo', type=FileStorage, location='files', required=True, help='Archivo zip')
diag_parser_rodilla.add_argument('sensacion_inestabilidad', type=bool, required=True, help='Sensacion de inestabilidad')
diag_parser_rodilla.add_argument('CA_positiva', type=bool, required=True, help='Prueba del "Cajon anterior" positiva')
diag_parser_rodilla.add_argument('impotencia_funcional', type=bool, required=True, help='Impotencia funcional')
diag_parser_rodilla.add_argument('id_usuario', type=int, required=True, help='ID de usuario')
diag_parser_rodilla.add_argument('dni_medico', type=str, required=True, help='DNI de médico')
diag_parser_rodilla.add_argument('fecha_nacimiento', type=str, required=True, help='Fecha de nacimiento del paciente')
diag_parser_rodilla.add_argument('peso', type=int, required=True, help='Peso del pacietnte en KG')
diag_parser_rodilla.add_argument('altura', type=int, required=True, help='Altura del paciente en CM')
diag_parser_rodilla.add_argument('sexo', type=str, required=True, help='Sexo del paciente')


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
    'password': fields.String(required=True, description='Contraseña del usuario')
})

login_model_response = api.model('Usuario', {
    'id': fields.Integer(description='ID del usuario'),
    'nombre': fields.String(description='Nombre del usuario'),
    'rol_id': fields.Integer(description='ID del rol del usuario'),
    'dni': fields.String(description='DNI del usuario'),
    'email': fields.String(description='Correo electrónico del usuario'),
    'especialidad': fields.String(description='Especialidad del usuario'),
    'establecimiento_id': fields.String(description='establecimiento_id del usuario'),
    'token': fields.String(description='Token de acceso')

})

verificar_codigo_model =  parser = reqparse.RequestParser()
parser.add_argument('codigo', type=str, required=True, help='Código OTP de 6 dígitos')

feedback_cerebro_args = reqparse.RequestParser()
feedback_cerebro_args.add_argument('imagen_id', type=int, required=True, help='Imagen id')
feedback_cerebro_args.add_argument('glioma', type=bool, required=False, help='glioma')
feedback_cerebro_args.add_argument('meningioma', type=bool, required=False, help='meningioma')
feedback_cerebro_args.add_argument('pituitary', type=bool, required=False, help='pituitary')
feedback_cerebro_args.add_argument('no_tumor', type=bool, required=False, help='no_tumor')
feedback_cerebro_args.add_argument('comentario', type=str, required=False, help='Comentario del médico')

feedback_pulmones_args = reqparse.RequestParser()
feedback_pulmones_args.add_argument('imagen_id', type=int, required=True, help='Imagen id')
feedback_pulmones_args.add_argument('pneumonia', type=bool, required=False, help='pneumonia')
feedback_pulmones_args.add_argument('no_pneumonia', type=bool, required=False, help='no_pneumonia')
feedback_pulmones_args.add_argument('comentario', type=str, required=False, help='Comentario del médico')

feedback_riñones_args = reqparse.RequestParser()
feedback_riñones_args.add_argument('imagen_id', type=int, required=True, help='Imagen id')
feedback_riñones_args.add_argument('quiste', type=bool, required=False, help='quiste')
feedback_riñones_args.add_argument('piedra', type=bool, required=False, help='piedra')
feedback_riñones_args.add_argument('tumor', type=bool, required=False, help='tumor')
feedback_riñones_args.add_argument('normal', type=bool, required=False, help='normal')
feedback_riñones_args.add_argument('comentario', type=str, required=False, help='Comentario del médico')

feedback_corazon_args = reqparse.RequestParser()
feedback_corazon_args.add_argument('imagen_id', type=int, required=True, help='Imagen id')
feedback_corazon_args.add_argument('contraccion_ventricular_prematura', type=bool, required=False, help='Contracción ventricular prematura')
feedback_corazon_args.add_argument('fusion_de_latido_ventricular_y_normal', type=bool, required=False, help='Fusión de latido ventricular y normal')
feedback_corazon_args.add_argument('infarto_de_miocardio', type=bool, required=False, help='Infarto de miocardio')
feedback_corazon_args.add_argument('latido_no_clasificable', type=bool, required=False, help='Latido no clasificable')
feedback_corazon_args.add_argument('latido_normal', type=bool, required=False, help='Latido normal')
feedback_corazon_args.add_argument('latido_prematuro_supraventricular', type=bool, required=False, help='Latido prematuro supraventricular')
feedback_corazon_args.add_argument('comentario', type=str, required=False, help='Comentario del médico')

feedback_rodilla_args = reqparse.RequestParser()
feedback_rodilla_args.add_argument('imagen_id', type=int, required=True, help='Imagen id')
feedback_rodilla_args.add_argument('rotura_lca', type=bool, required=False, help='rotura_lca')
feedback_rodilla_args.add_argument('lca_sano', type=bool, required=False, help='lca_sano')
feedback_rodilla_args.add_argument('comentario', type=str, required=False, help='Comentario del médico')

feedback_muñeca_args = reqparse.RequestParser()
feedback_muñeca_args.add_argument('imagen_id', type=int, required=True, help='Imagen id')
feedback_muñeca_args.add_argument('etiqueta 1', type=bool, required=False, help='etiqueta 1')
feedback_muñeca_args.add_argument('etiqueta 2', type=bool, required=False, help='etiqueta 2')
feedback_muñeca_args.add_argument('comentario', type=str, required=False, help='Comentario del médico')