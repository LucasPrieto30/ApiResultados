from database.dto_medico import insert_medico

class CrudMedico:
    def crear_medico(self, datos_medico):
        nuevo_medico = {
            "id": datos_medico.get("id"),
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
