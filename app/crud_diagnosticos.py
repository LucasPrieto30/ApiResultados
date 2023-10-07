import json

class CrudDiagnostico:
    def __init__(self):
        # Simulación de una lista de diagnósticos
        try:
            with open("diagnosticos.json", "r") as archivo_json:
                self.diagnosticos = json.load(archivo_json)
        except (FileNotFoundError, json.JSONDecodeError):
            self.diagnosticos = []

    def crear_diagnostico(self, datos_diagnostico):
        # Lógica para crear un diagnóstico y agregarlo a la lista
        nuevo_diagnostico = {
            "ID_user": datos_diagnostico.get("ID_user"),
            "Edad": datos_diagnostico.get("Edad"),
            "Peso": datos_diagnostico.get("Peso"),
            "Altura cm": datos_diagnostico.get("Altura cm"),
            "Sexo": datos_diagnostico.get("Sexo"),
            "Sección del cuerpo": datos_diagnostico.get("Sección del cuerpo"),
            "condiciones previas": datos_diagnostico.get("condiciones previas"),
            "Imagen": datos_diagnostico.get("Imagen")
        }
        nuevo_diagnostico = {"id": len(self.diagnosticos) + 1, **datos_diagnostico}
        self.diagnosticos.append(nuevo_diagnostico)
        self.guardar_diagnosticos_en_json()
        return nuevo_diagnostico

    def obtener_diagnostico(self, id_diagnostico):
        # Lógica para obtener un diagnóstico de la lista por su ID
        for diagnostico in self.diagnosticos:
            if diagnostico["id"] == id_diagnostico:
                # Obtener el ID_user y el ID_rol correspondientes al diagnóstico
                ID_user = diagnostico.get("ID_user")
                ID_rol = diagnostico.get("ID_rol")

                datos_diagnostico = {
                    "id": diagnostico.get("id"),
                    "ID_user": ID_user,
                    "ID_rol": ID_rol,
                    "diagnostico/resultados": {
                        "Edad": diagnostico.get("Edad"),
                        "Peso": diagnostico.get("Peso"),
                        "Altura cm": diagnostico.get("Altura cm"),
                        "Sexo": diagnostico.get("Sexo"),
                        "Sección del cuerpo": diagnostico.get("Sección del cuerpo"),
                        "condiciones previas": diagnostico.get("condiciones previas"),
                        "Imagen": diagnostico.get("Imagen")
                    }
                }
                return datos_diagnostico
        return None

    ## si se pide a futuro
    def actualizar_diagnostico(self, id_diagnostico, nuevos_datos):
        # Lógica para actualizar un diagnóstico en la lista por su ID
        for diagnostico in self.diagnosticos:
            if diagnostico["id"] == id_diagnostico:
                diagnostico.update(nuevos_datos)
                #self.guardar_diagnosticos_en_json()

                return diagnostico
        return None
    ## si se pide a futuro
    def eliminar_diagnostico(self, id_diagnostico):
        # Lógica para eliminar un diagnóstico de la lista por su ID
        for diagnostico in self.diagnosticos:
            if diagnostico["id"] == id_diagnostico:
                self.diagnosticos.remove(diagnostico)
                #self.guardar_diagnosticos_en_json()

                return True
        return False

    def mostrar_diagnosticos(self):
        lista_diagnosticos = []
        for diagnostico in self.diagnosticos:
            # Obtener el ID_user y el ID_rol correspondientes al diagnóstico
            ID_user = diagnostico.get("ID_user")
            ID_rol = diagnostico.get("ID_rol")

            datos_diagnostico = {
                "id": diagnostico.get("id"),
                "ID_user": ID_user,
                "ID_rol": ID_rol,
                "diagnostico/resultados": {
                    "Edad": diagnostico.get("Edad"),
                    "Peso": diagnostico.get("Peso"),
                    "Altura cm": diagnostico.get("Altura cm"),
                    "Sexo": diagnostico.get("Sexo"),
                    "Sección del cuerpo": diagnostico.get("Sección del cuerpo"),
                    "condiciones previas": diagnostico.get("condiciones previas"),
                    "Imagen": diagnostico.get("Imagen")
                }
            }
            lista_diagnosticos.append(datos_diagnostico)
        return lista_diagnosticos
    
##------metodos auxiliares--------##

    # Método para guardar la lista de diagnósticos en el archivo JSON
    def guardar_diagnosticos_en_json(self):
        with open("diagnosticos.json", "w") as archivo_json:
            json.dump(self.diagnosticos, archivo_json)

    def resetear_diagnosticos(self):
        self.diagnosticos = []  # Reiniciar la lista de diagnósticos
        self.guardar_diagnosticos_en_json()  # Guardar la lista vacía en el archivo JSON
        if len(self.diagnosticos) == 0:
            return True
        else:
            return False
        