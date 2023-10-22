from flask_restx import Resource, Namespace, fields
from .modelos import post_model, pacienteDiagnostico, post_model2, post_medico
from flask import jsonify, request
from app.models.entities.Historial import Historial
from database.db import get_connection
from werkzeug.utils import secure_filename
import os
from psycopg2 import Binary
import requests
from .crud_medico import CrudMedico

from flask_restx import Api


api = Api()

ns_usuarios = Namespace("Usuarios")

user_parser = api.parser()
user_parser.add_argument('nombre', type=str, required=True, help='Nombre')
user_parser.add_argument('dni', type=str, required=True, help='DNI')
user_parser.add_argument('new_dni', type=str, required=True, help='Nuevo DNI')
user_parser.add_argument('password', type=str, required=True, help='Contraseña')
user_parser.add_argument('rol_id', type=int, required=True, help='Rol ID')
user_parser.add_argument('establecimiento_id', type=int, required=True, help='Id del establecimiento')


crud2 = CrudMedico()
@ns_usuarios.route('/medicos')
class Medicos(Resource):
    def get(self):
        try:
           connection = get_connection()
           with connection.cursor() as cursor: 
                consulta = "SELECT u.id AS id, u.nombre AS nombre, u.rol_id AS rol_id, e.id AS establecimiento_id, e.nombre AS establecimiento_nombre, e.direccion AS establecimiento_direccion FROM public.usuario AS u JOIN public.establecimiento AS e ON u.establecimiento_id = e.id where u.rol_id = 4;"
                cursor.execute(consulta)
                resultados = cursor.fetchall()
                medicos = []
                for resultado in resultados:
                    usuario = {
                        'id': resultado[0],
                        'nombre': resultado[1],
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
            return jsonify({"message": str(ex.__cause__)}),500

@ns_usuarios.route("")
class MedicoCreate(Resource):
    @ns_usuarios.expect(post_medico)
    @ns_usuarios.doc(responses={201: 'Éxito', 500: 'Error al enviar el medico'})
    def post(self):
        # tener los datos del medico del cuerpo de la solicitud
            nuevo_medico = ns_usuarios.payload
            # Llama al método para crear un medico en el CRUD
            resultado = crud2.crear_medico(nuevo_medico)
            if resultado.get("success", False):
                return resultado, 201  # Devuelve el médico creado y el código 201 (Created)
            else:
                return {"error": resultado.get("message", "No se pudo crear el médico")}, 500  # En caso de error

@ns_usuarios.route("/<int:id>")
class Medico(Resource):
    #@ns_usuarios.expect(parser)
    @ns_usuarios.doc(responses={200: 'Éxito', 401: 'Acceso no autorizado', 404: 'Médico no encontrado'})
    def get(self, id):
        #args = parser.parse_args()  # Analiza los argumentos de la solicitud
        # Obtén el ID y la clave de los argumentos
        medico_id = id
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
        medico = crud2.consultar_medico_por_id(medico_id)
        if medico:
            try:
                response = {
                "success": True,
                "medico": medico
                }
                return response ,200
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

@ns_usuarios.route('/admin/alta')
class Usuarios(Resource):
    @ns_usuarios.expect(user_parser)
    def post(self):
        try:
            
            args = user_parser.parse_args()

            nombre = args['nombre']
            dni = args['dni']
            password = args['password']
            rol_id = args['rol_id']
            establecimiento_id = args['establecimiento_id']

            connection = get_connection()
            with connection.cursor() as cursor:
                
                consulta = "INSERT INTO public.usuario (nombre, dni, password, rol_id, establecimiento_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;"
                cursor.execute(consulta, (nombre, dni, password, rol_id, establecimiento_id))
                new_user_id = cursor.fetchone()[0]
                connection.commit()

            cursor.close()
            connection.close()

            return {"message": "Agregado exitosamente", "user_id": new_user_id}, 201

        except Exception as ex:
            return {"message": str(ex)}, 500





@ns_usuarios.route('/usuarios/<string:dni>')
class Usuario(Resource):
    def delete(self, dni):
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
    @ns_usuarios.expect(user_parser)
    def patch(self):
        try:
            args = user_parser.parse_args()

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
                    update_sql += " password = %s,"
                    params.append(new_password)
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
        