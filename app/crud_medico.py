from database.dto_medico import insert_medico, consultar_medico_id

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

    def comparar_RolUsuario(numero):
        if numero == 1:
            return "La entrada es igual a 1"
        elif numero == 2:
            return "La entrada es igual a 2"
        elif numero == 3:
            return "La entrada es igual a 3"
        elif numero == 4:
            return "La entrada es igual a 4"
        else:
            return "La entrada no está en el rango del 1 al 4"
