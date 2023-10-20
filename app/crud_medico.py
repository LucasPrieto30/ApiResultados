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
'''     if medico:
            datos_medico = {
                "id": medico.get("id"),
                "nombre": medico.get("nombre"),
                "dni": medico.get("dni"),  # Agrega la lógica para obtener el DNI si está disponible.
                "email": medico.get("email"),
                "password": medico.get("password"),
                "rol_id": medico.get("rol_id"),  # Agrega la lógica para obtener el rol_id si está disponible.
                "establecimiento_id": medico.get("establecimiento_id"),  # Agrega la lógica para obtener el establecimiento_id si está disponible.
                "fecha_ultima_password": medico.get("fecha_ultima_password"),  # Agrega la lógica para obtener la fecha_ultima_password si está disponible.
                "especialidad": medico.get("especialidad")
            }
'''
