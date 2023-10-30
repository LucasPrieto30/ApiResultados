from database.dto_medico import insert_medico, consultar_medico_id
import re
class CrudMedico:
    def crear_medico(self, datos_medico):
        nuevo_medico = {
            "nombre": datos_medico.get("nombre"),
            "dni": datos_medico.get("dni"),
            "email": datos_medico.get("email"),
            "password": datos_medico.get("password"),
            "rol_id": datos_medico.get("rol_id"),
            "establecimiento_id": datos_medico.get("establecimiento_id"),
            "fecha_ultima_password": datos_medico.get("fecha_ultima_password"),
            "especialidad": datos_medico.get("especialidad")
        }  
        #if insert_medico(nuevo_medico):
        return insert_medico(nuevo_medico)
        #else:
        #   return False
    def consultar_medico_por_id(self, id_medico):
        medico  = consultar_medico_id(id_medico)
        return medico

def validar_contrasena(contrasena):
    if len(contrasena) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not any(c.isupper() for c in contrasena):
        return "La contraseña debe contener al menos una letra mayúscula."
    if not any(c.islower() for c in contrasena):
        return "La contraseña debe contener al menos una letra minúscula."
    if not any(c.isdigit() for c in contrasena):
        return "La contraseña debe contener al menos un número."
    caracteres_especiales_permitidos = "!@#$%^&*()_+{}[]:;<>,.?~|/"
    if not any(c in caracteres_especiales_permitidos for c in contrasena):
        return "La contraseña debe contener al menos un carácter especial (por ejemplo, !@#$%^&*()_+{}[]:;<>,.?~|/)."
    caracteres_no_validos_permitidos = "↓↑→↨←§∟↔*"
    if any(c in contrasena for c in caracteres_no_validos_permitidos):
        return "La contraseña contiene caracteres no válidos."

    return None  # La contraseña es válida