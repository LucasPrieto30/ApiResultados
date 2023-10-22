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
