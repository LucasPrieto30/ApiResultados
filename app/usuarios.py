import base64
from flask_restx import Resource, Namespace, fields
import pyotp
from .modelos import post_model, pacienteDiagnostico, post_model2, post_medico, login_model, login_model_response, verificar_codigo_model,reset_password_model,verify_code_parser,reset_password_parser
from flask import jsonify, request, session
from database.db import get_connection
from werkzeug.utils import secure_filename
import os
import pytz
from psycopg2 import Binary
import requests
from .crud_medico import CrudMedico , validar_contrasena
from flask_restx import Api
from database.dto_medico import obtener_clave_desde_Medico, checkUsuarioPorDni, verificarPassword, get_ultimo_cambio_pass, guardar_codigo, borrar_codigo,set_code, checkUsuarioPorDni_reset,identify_user_by_reset_token,reset_user_password
import argparse
import datetime
import re
from .correo import enviar_codigo_correo, enviar_codigo_correo_reset
from app.jwt_config import require_auth, generate_token, verify_token
import random
import uuid

SECRET_KEY = 'dtcp23'
# Convertir la clave secreta a bytes
secret_bytes = SECRET_KEY.encode('utf-8')

# Codificar en base32
secret_base32 = base64.b32encode(secret_bytes).decode('utf-8')
# Crear una instancia del generador de OTP
otp_generator = pyotp.TOTP(secret_base32, interval=60)

api = Api()

ns_usuarios = Namespace("Usuarios")

user_parser = api.parser()
user_parser.add_argument('nombre', type=str, required=True, help='Nombre')
user_parser.add_argument('apellido', type=str, required=True, help='Apellido')
user_parser.add_argument('dni', type=str, required=True, help='DNI')
user_parser.add_argument('email', type=str, required=True, help='email')
#user_parser.add_argument('fecha_ultima_password', type=str, required=True, help='fecha')
#user_parser = argparse.ArgumentParser(description='Descripción de tu programa')
#fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#user_parser.add_argument('fecha_ultima_password', type=str, default=fecha_actual, help='Fecha de última contraseña')
#user_parser.add_argument('fecha_ultima_password', type=str, required=True, help='Nuevo fecha')
user_parser.add_argument('password', type=str, required=True, help='Contraseña')
user_parser.add_argument('rol_id', type=int, required=True, help='Rol ID')
user_parser.add_argument('establecimiento_id', type=int, required=False, help='Id del establecimiento')
user_parser.add_argument('especialidad', type=str, required=True, help='especialidad')

user_parser_update = api.parser()
user_parser_update.add_argument('dni', type=str, required=True, help='DNI')
user_parser_update.add_argument('new_dni', type=str, required=False, help='Nuevo DNI')
user_parser_update.add_argument('nombre', type=str, required=False, help='Nombre')
user_parser_update.add_argument('password', type=str, required=False, help='Contraseña')
user_parser_update.add_argument('rol_id', type=int, required=False, help='Rol ID')
user_parser_update.add_argument('establecimiento_id', type=int, required=False, help='Id del establecimiento')
user_parser_update.add_argument('especialidad', type=str, required=False, help='especialidad')



crud2 = CrudMedico()

@ns_usuarios.route('/medicos')
@ns_usuarios.doc(responses={200: 'Éxito', 500: 'Error interno del servidor'})
class Medicos(Resource):
    @require_auth
    def get(self,payload):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                consulta = "SELECT u.id AS id, u.nombre AS nombre, u.rol_id AS rol_id, e.id AS establecimiento_id, e.nombre AS establecimiento_nombre, e.direccion AS establecimiento_direccion FROM public.usuario AS u JOIN public.establecimiento AS e ON u.establecimiento_id = e.id where u.rol_id = 4;"
                cursor.execute(consulta)
                resultados = cursor.fetchall()
                medicos = []
                for resultado in resultados:
                    if ', ' in resultado[1]:
                        apellido, nombre = resultado[1].split(', ')
                    else:
                        apellido, nombre = '', resultado[1]
                    usuario = {
                        'id': resultado[0],
                        'nombre': nombre,
						'apellido': apellido,
                        'rol_id': resultado[2],
                        'establecimiento_id': resultado[3],
                        'establecimiento_nombre': resultado[4],
                        'establecimiento_direccion': resultado[5]
                    }
                    medicos.append(usuario)

                cursor.close()
                connection.close()
                return medicos, 200
        except Exception as ex:
            return jsonify({"message": str(ex.__cause__)}), 500

# @ns_usuarios.route("")
# class MedicoCreate(Resource):
# 	@ns_usuarios.expect(post_medico)
# 	@ns_usuarios.doc(responses={201: 'Éxito', 500: 'Error al enviar el medico'})
# 	def post(self):
# 		# tener los datos del medico del cuerpo de la solicitud
# 			nuevo_medico = ns_usuarios.payload
# 			# Llama al método para crear un medico en el CRUD
# 			resultado = crud2.crear_medico(nuevo_medico)
# 			if resultado.get("success", False):
# 				return resultado, 201  # Devuelve el médico creado y el código 201 (Created)
# 			else:
# 				return {"error": resultado.get("message", "No se pudo crear el médico")}, 500  # En caso de error

@ns_usuarios.route("/<int:id>")
class Medico(Resource):
	#@ns_usuarios.expect(parser)
	@ns_usuarios.doc(security=None)
	@ns_usuarios.doc(responses={200: 'Éxito', 401: 'Acceso no autorizado', 404: 'Médico no encontrado'})
	def get(self,id):
		#args = parser.parse_args()  # Analiza los argumentos de la solicitud
		# Obtén el ID y la clave de los argumentos
		usuario_id = id
		#clave = args['clave'].encode('utf-8')
		#clave_ingresada = clave.encode('utf-8')
		#CLAVE_REQUERIDA_str = CLAVE_REQUERIDA.decode('utf-8')
		#CLAVE_REQUERIDA_str = CLAVE_REQUERIDA.decode('utf-8')
		#print(clave)
		#print(CLAVE_REQUERIDA)
		#if isinstance(clave, bytes):
	# La clave se ha guardado como bytes
		 #   print("La clave maestra es de tipo bytes.",clave)
		#Obtén la clave proporcionada por el usuario desde los parámetros de consulta
		#clave = ns.payload.get('clave')  # Obtén la clave de la solicitud GET
		# Verifica si la clave proporcionada coincide con la clave requerida
		#if clave != CLAVE_REQUERIDA:
		 #   return {"error": "Acceso no autorizado"}, 401  # Devuelve un error 401 (No autorizado) si la clave no coincide
		# Realiza una consulta en la base de datos para obtener los datos del médico con el ID proporcionado (id)
		usuario = crud2.consultar_medico_por_id(usuario_id)
		if usuario:
			try:
				response = usuario
				return response, 200
			except Exception as e:
				response = {
					"success": False,
					"message": "Error al desencriptar el correo: " + str(e)
				}
			return response, 500  # Devuelve una respuesta de error con el código 500 en caso de error de desencriptación
		else:
			# Descifra el correo y la contraseña antes de mostrarlos
			#medico['correo_electronico'] = crud2.descifrar_valor(medico['correo_electronico'],clave)
			#medico['contrasena'] = crud2.descifrar_valor(medico['contrasena'],clave)
			#return medico, 200  # Devuelve los datos del médico y el código 200 (OK)
			response = {
			"success": True,
			"message": "No se encontró ningún médico con ese ID"
			}

			return response, 404  # Devuelve un error 404 si el médico no se encuentra

import psycopg2
#@ns_usuarios.route('/admin/alta') se cambio
@ns_usuarios.route('/registro')
class Usuarios(Resource):
	@ns_usuarios.doc(security=None)
	@ns_usuarios.expect(user_parser)
	@ns_usuarios.doc(responses={201: 'Agregado exitosamente', 409: 'El usuario ya está registrado', 400: 'Solicitud inválida', 500: 'Error interno del servidor'})
	def post(self):
		try:
			args = user_parser.parse_args()
			#Define el email y la clave
			email = args['email'].lower()
			clave = obtener_clave_desde_Medico()
			#resultado = f"pgp_sym_encrypt('{email}', '1', 'compress-algo=0,cipher-algo=AES128')"
			#arg1 = "1"
			arg2 = "compress-algo=0,cipher-algo=AES128"
			#pgp_sym_encrypt_string = f"pgp_sym_encrypt('{email}', '{arg1}', '{arg2}')"
			
			nombre = args['nombre']
			dni = args['dni']
			apellido = args['apellido']
			nombre_apellido = f"{apellido}, {nombre}"
			password = args['password']
			rol_id = args['rol_id']
			establecimiento_id = args['establecimiento_id']

			zona_horaria_argentina = pytz.timezone('America/Argentina/Buenos_Aires')

			# Obtiene la fecha y hora actual en la zona horaria de Argentina
			fecha_hora_argentina = datetime.datetime.now(zona_horaria_argentina)
			# Obtener la fecha actual
			fecha_ultima_password = fecha_hora_argentina.strftime('%Y-%m-%d %H:%M:%S')
			especialidad = args['especialidad']      
			error = validar_contrasena(password)
			if error is not None:
				return {"message": error}, 400
			
			connection = get_connection()
			with connection.cursor() as cursor:
				#print('priemro')
				if not dni.isdigit():
					return {"message": "DNI debe ser una cadena de números"}, 400
				if not re.match(r"[^@]+@[^@]+\.[a-z]+", email):
					return {"message": "Formato de email no válido"}, 400
				cursor.execute("SELECT id FROM usuario WHERE dni = %s;", (dni,)) 
				UsuarioExistente = cursor.fetchone()
				if UsuarioExistente:
					#print("dentro")
					return {"message": "El Usuario DNI ya está registrado."}, 409
				#print("hola")
				#cursor.execute("SELECT COUNT(*) FROM usuario WHERE id>=77 and %s = pgp_sym_decrypt(email::bytea, %s, %s)::text;", (email,clave, arg2))
				cursor.execute("SELECT EXISTS (SELECT 1 FROM usuario WHERE id >= 77 AND pgp_sym_decrypt(email::bytea, %s, %s) = %s) AS existe_correo;", (clave, arg2, email))
				correoExistente= cursor.fetchone()[0]
				if correoExistente:
					return {"message": "Usuario email ya existe"}, 409
					
				consulta = "INSERT INTO public.usuario (nombre, dni, email, password, rol_id, establecimiento_id, fecha_ultima_password, especialidad) VALUES (%s, %s,pgp_sym_encrypt(%s, %s, %s), %s, %s, %s, %s, %s) RETURNING id;"
				cursor.execute(consulta, (nombre_apellido, dni, email, clave,arg2, password, rol_id, establecimiento_id, fecha_ultima_password, especialidad))
				new_user_id = cursor.fetchone()[0]
				connection.commit()
				if (rol_id == 4):
					cursor.execute("UPDATE public.diagnostico SET usuario_medico_id = %s where usuario_medico_id IS NULL AND usuario_medico_dni = %s", (new_user_id, dni))
					connection.commit()
			cursor.close()
			connection.close()

			return {"message": "Agregado exitosamente", "user_id": new_user_id}, 201

		except psycopg2.Error as ex:
    # Manejar excepciones específicas de PostgreSQL aquí
			return {"message": str(ex)}, 500



@ns_usuarios.route('/<string:dni>')
class Usuario(Resource):
	@ns_usuarios.doc(security=None)
	@ns_usuarios.doc(responses={200: 'Borrado exitosamente', 404: 'Médico no encontrado', 500: 'Error interno del servidor'})
	def delete(self ,dni):
		try:
			connection = get_connection()
			with connection.cursor() as cursor:
				cursor.execute("SELECT id FROM public.usuario WHERE dni = %s", (dni,))
				existing_user = cursor.fetchone()
				if not existing_user:
					return {"message": "No encontrado"}, 404  

				# Borro ususario por dni
				cursor.execute("DELETE FROM public.usuario WHERE  dni = %s", (dni,))
				connection.commit()

			cursor.close()
			connection.close()

			return {"message": "Borrado exitosamente"}, 200

		except Exception as ex:
			return {"message": str(ex)}, 500
				
		
@ns_usuarios.route('/update-user-informacion', methods=['PATCH'])
class UpdateUserInfo(Resource):
	@ns_usuarios.doc(security=None)
	@ns_usuarios.doc(responses={200: 'Información de usuario actualizada', 404: 'Médico no encontrado', 500: 'Error interno del servidor'})
	@ns_usuarios.expect(user_parser_update)
	def patch(self):
		try:
			args = user_parser_update.parse_args()
			dni = args['dni']

			new_nombre = args['nombre']
			new_dni = args['new_dni']
			new_password = args['password']
			new_rol_id = args['rol_id']
			new_establecimiento = args['establecimiento_id']

			connection = get_connection()
			with connection.cursor() as cursor:
				cursor.execute("SELECT id FROM public.usuario WHERE dni = %s", (dni,))
				existing_user = cursor.fetchone()
				if not existing_user:
					return {"message": "No encontrado"}, 404  
				update_sql = "UPDATE public.usuario SET"
				params = []
				if new_nombre:
					update_sql += " nombre = %s,"
					params.append(new_nombre)
				if new_dni:
					update_sql += " dni = %s,"
					params.append(new_dni)
				if new_password:
					zona_horaria_argentina = pytz.timezone('America/Argentina/Buenos_Aires')
					# Obtiene la fecha y hora actual en la zona horaria de Argentina
					fecha_hora_argentina = datetime.datetime.now(zona_horaria_argentina)
					# Obtener la fecha actual
					fecha_ultima_password = fecha_hora_argentina.strftime('%Y-%m-%d %H:%M:%S')
					update_sql += " password = %s, fecha_ultima_password = %s,"
					params.append(new_password)
					params.append(fecha_ultima_password)
				if new_rol_id:
					update_sql += " rol_id = %s,"
					params.append(new_rol_id)
				if new_establecimiento:
					update_sql += " establecimiento_id = %s,"
					params.append(new_establecimiento)

				update_sql = update_sql.rstrip(',') + " WHERE dni = %s;"
				params.append(dni)

				cursor.execute(update_sql, params)
				connection.commit()

			cursor.close()
			connection.close()

			return {"message": "Informacion de usuario actualizada"}, 200

		except Exception as ex:
			return {"message": str(ex)}, 500


login_model_response = ns_usuarios.model('LoginResponse', {
    'token': fields.String(description='Token de acceso'),
    'id': fields.Integer(description='ID del usuario'),
    'nombre': fields.String(description='Nombre del usuario'),
	'apellido': fields.String(description='Apellido del usuario'),
    'rol_id': fields.Integer(description='ID del rol del usuario'),
    'dni': fields.String(description='DNI del usuario'),
    'email': fields.String(description='Email del usuario'),
    'especialidad': fields.String(description='Especialidad del usuario'),
    'establecimiento_id': fields.Integer(description='ID del establecimiento del usuario'),
})

# Define el modelo para las solicitudes del recurso Login
login_model = ns_usuarios.model('LoginModel', {
    'dni': fields.String(required=True, description='DNI del usuario'),
    'password': fields.String(required=True, description='Contraseña'),
})
#@ns_usuarios.response(200, 'Correcto. Bienvenido', login_model_response)
#@ns_usuarios.response(401, 'Contraseña incorrecta')
#@ns_usuarios.response(404, 'Usuario inexistente')
@ns_usuarios.route('/login')
class Login(Resource):
	@ns_usuarios.doc(security=None)
	@ns_usuarios.response(200, 'Correcto. Bienvenido', login_model_response)
	@ns_usuarios.response(401, 'Contraseña incorrecta')
	@ns_usuarios.response(404, 'Usuario inexistente')
	@ns_usuarios.expect(login_model, validate=True)
	def post(self):
		args = ns_usuarios.payload
		dni = args['dni']
		password = args['password']
		usuarioExistente = checkUsuarioPorDni(dni)
		if not dni or not password:
			return {'message': 'Por favor, ingrese DNI y contraseña'}, 400
		if usuarioExistente:
			# Verificar si el usuario tiene una contraseña valida (no expirada)
			# if not validPassword(usuarioExistente[1]):
			# 	return {'message' : 'La contraseña ha expirado'}, 403
			if ', ' in usuarioExistente[1]:
				apellido, nombre = usuarioExistente[1].split(', ')
			else:
				apellido, nombre = '', usuarioExistente[1]
			usuario = {
					'id': usuarioExistente[0],
					'nombre': nombre,
					'apellido': apellido,
					'rol_id': usuarioExistente[2],
					'dni': usuarioExistente[3],
					'email': usuarioExistente[4],
					'especialidad': usuarioExistente[6],
					'establecimiento_id': usuarioExistente[7],
				}
			ultimo_cambio_pass = get_ultimo_cambio_pass(usuarioExistente[3])
			# Comprobar que la contraseña es correcta
			if not verificarPassword(password, usuarioExistente):
				return {'message' : 'Contraseña incorrecta'}, 401
			elif ultimo_cambio_pass is not None: 
				cant_dias = (datetime.datetime.now() - ultimo_cambio_pass).days 
				if cant_dias>= 60: 
					return {"message": "Es necesario cambiar la contraseña."},401
			#si el usuario es auditor o admin, se le envia un codigo de verificacion por mail
				elif usuarioExistente[2] == 1 or usuarioExistente[2] == 2:
					codigo_otp = otp_generator.now()
					if guardar_codigo(codigo_otp, usuarioExistente[3]):
						enviar_codigo_correo(usuarioExistente[4], codigo_otp)
			
			token = generate_token(usuario)

			# Incluir el token en la respuesta
			usuario_data = {
				'token': token,
				'id': usuarioExistente[0],
				'nombre': nombre,
				'apellido': apellido,
				'rol_id': usuarioExistente[2],
				'dni': usuarioExistente[3],
				'email': usuarioExistente[4],
				'especialidad': usuarioExistente[6],
				'establecimiento_id': usuarioExistente[7],
			}
			return usuario_data, 200
		return {'message' : 'Usuario inexistente'}, 404

@ns_usuarios.route('/verificacion')
class VerificarCodigo(Resource):
	@ns_usuarios.doc(security=None)
	@ns_usuarios.doc(responses={200: 'Código válido', 401: 'Código inválido'})
	@ns_usuarios.expect(verificar_codigo_model)
	def post(self):
			args = verificar_codigo_model.parse_args()
			dni = args['dni']
			codigo = args['codigo']
			
			try:
				connection = get_connection()
				with connection.cursor() as cursor:
					cursor.execute("SELECT * FROM public.usuario WHERE dni = %s", (dni,))
					user = cursor.fetchone()
					if user is None:
						return {'msg': 'Usuario inexistente'}, 404
					else:
						cursor.execute("SELECT verify_code FROM public.usuario WHERE dni = %s", (dni,))
						resultado = cursor.fetchone()
						cod_db= resultado[0]
						connection.close() 
				
					if cod_db:
						# Verificar el código OTP 
						if cod_db == codigo: 
							borrar_codigo(dni)
							# El código es válido y corresponde al usuario 
							return {'msg': 'Código válido'}, 200
						else:
							return {'msg': 'Código inválido'}, 401
			except Exception as ex:
				return {"message": str(ex)}, 500	

from flask import request
import jwt
# Crear una nueva instancia de Namespace si aún no la tienes
# ns_usuarios = Namespace('usuarios', description='Namespace para usuarios')
verificacion_token_model = ns_usuarios.model('VerificacionTokenModel', {
    'token': fields.String(description='Token de autenticación')
})

@ns_usuarios.route('/verificarUsuario')
class VerificarToken(Resource):
    @ns_usuarios.doc(security=None)
    @ns_usuarios.expect(verificacion_token_model)
    @ns_usuarios.doc(responses={200: 'Token valido', 500: 'Error interno del servidor', 401: 'Token invalido'})
    def post(self):
        token = request.json.get('token')  # Obtener el token del cuerpo de la solicitud
        if verify_token(token):
            payload = jwt.decode(token, obtener_clave_desde_Medico(), algorithms=['HS256'])
            #print(payload['dni'])
            # como es valido le doy los datos
            return payload['dni'], 200
        else:
            return {'token': 'Token inválido o faltante'}, 401

@ns_usuarios.route('/reset_pass/<string:dni>')
class reset_password(Resource):    
	def post(self,dni):
		usuarioExistente = checkUsuarioPorDni_reset(dni) 
		if not dni:
			return {'message': 'Por favor, ingrese DNI'}, 400
		if usuarioExistente:
			codigo_reset = random.randint(1000, 9999)
			set_code(codigo_reset,dni)
			print(f"Done")
			enviar_codigo_correo_reset(usuarioExistente[4], codigo_reset)
			print(f"Done")
			return {'message' : 'Mensaje enviado correctamente'}, 200
		return {'message' : 'Usuario inexistente'}, 404
	

@ns_usuarios.route('/reset_password_new/')
class ResetPassword(Resource):
    @ns_usuarios.expect(reset_password_model)
    def post(self):
        args = reset_password_model.parse_args()
        dni = args['dni']
        codigo = args['codigo']
        new_password = args['new_password']
        confirm_password = args['confirm_password']

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT reset_code FROM public.usuario WHERE dni = %s", (dni,))
                codigoreset = cursor.fetchone()
                codigoreset = codigoreset[0] if codigoreset else None
                cursor.close()
                
            if codigoreset == codigo:
                error = validar_contrasena(new_password)
                if error is not None:
                    return {"message": error}, 400
                elif new_password == confirm_password:
                    with connection.cursor() as cursor:
                        cursor.execute("UPDATE public.usuario SET reset_code = NULL, password = %s WHERE dni = %s;", (new_password, dni))
                        connection.commit()
                    return {'msg': 'Contraseña actualizada.'}, 200
                else:
                    return {'msg': 'Contraseñas no coinciden.'}, 400
            else:
                return {'msg': 'Codigo invalido'}, 401
        except Exception as ex:
            return {"message": str(ex)}, 500
        finally:
            connection.close()
            

def generate_temporary_token():
    token = str(uuid.uuid4())
    return token

@ns_usuarios.route('/check_code')
class VerifyCode(Resource):
    @ns_usuarios.expect(verify_code_parser)
    def post(self):
        args = verify_code_parser.parse_args()
        codigo = args['codigo']

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT reset_code, dni FROM public.usuario WHERE reset_code = %s", (codigo,))
                result = cursor.fetchone()
                if result:
                    dni = result[1]

                    session['reset_token'] = generate_temporary_token()
                    
                    cursor.execute("UPDATE usuario SET reset_token = %s WHERE reset_code = %s", (session['reset_token'], codigo))
                    connection.commit()
					
                    return {'msg': 'Codigo verificado exitosamente', 'dni': dni}, 200
                else:
                    return {'msg': 'Codigo invalido'}, 401
        except Exception as ex:
            return {"message": str(ex)}, 500
        finally:
            connection.close()


@ns_usuarios.route('/reset_password')
class ResetPassword(Resource):
    @ns_usuarios.expect(reset_password_parser)
    def post(self):
        args = reset_password_parser.parse_args()
        new_password = args['new_password']
        confirm_password = args['confirm_password']
        
        error = validar_contrasena(new_password)
        if error is not None:
            return {"message": error}, 400        
        try:            
            reset_token = session.get('reset_token')
            if reset_token:
                if new_password == confirm_password:        
                    user_dni = identify_user_by_reset_token(reset_token)
                    if user_dni:
                        reset_user_password(reset_token, new_password)

                        session.pop('reset_token', None)

                        return {'msg': 'Contraseña actualizada.'}, 200
                    else:
                        return {'msg': 'Token Invalido'}, 401
                else:
                    return {'msg': 'Contraseñas no coinciden.'}, 400
            else:
                return {'msg': 'Token Invalido'}, 401
        except Exception as ex:
            return {"message": str(ex)}, 500
