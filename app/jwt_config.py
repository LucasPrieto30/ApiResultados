from datetime import datetime, timedelta
from flask import logging, request
import jwt
from functools import wraps  # Importa functools.wraps para decoradores
from database.dto_medico import obtener_clave_desde_Medico
from flask import current_app


# generar un token JWT
def generate_token(dni):
    #expiration_time = datetime.utcnow() + timedelta(seconds=160)

    payload = {
        'dni': dni
        #'exp': expiration_time
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

#verificar un token JWT
def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # El token ha expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido

# Decorador para verificar la autenticación con JWT
#import jwt
#from flask import request

def require_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return {'message': 'Token JWT faltante'}, 401

        # Verifica si el token comienza con "Bearer "
        if not token.startswith('Bearer '):
            return {'message': 'Formato de token JWT inválido'}, 401

        # Elimina "Bearer " del encabezado del token
        token = token.split(' ')[1]

        # Verificar si el token es un JWT válido
        try:
            payload = jwt.decode(token, obtener_clave_desde_Medico(), algorithms=['HS256'])
            #print("hoa")
            #print(payload)
        except jwt.ExpiredSignatureError:
            return {'message': 'Token JWT expirado'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token JWT inválido'}, 401

        # Llama a func con el contenido del token como primer argumento
        return func(payload, *args, **kwargs)

    return decorated
