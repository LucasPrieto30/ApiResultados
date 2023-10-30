# ApiResultados
Api desarrollada en Flask para realizar conexion con el front y los modelos de machine learning.
Gestiona el acceso y manejo de usuarios, diagnosticos e historial
Esta desarrollada en Flask-restx, lo que nos proporciona una interfaz Swagger para una documentacion interactiva de los metodos desarrollados.

La API se encuentra hosteada en Render y se puede acceder a traves del siguiente enlace
https://api-resultados.onrender.com

## Endpoints

### Diagnosticos

En esta sección se encuentran los endpoints que manejan los diagnosticos, resultados e historial. Para realizar los diagnosticos/predicciones se conecta con APIS desarrolladas por los equipos de los modelos.

#### /Diagnosticos/predecir/cerebro [POST]

El objetivo de este endpoint es comunicarse con el modelo del cerebro para obtener las probabilidades de tener las distintas clases de tumores.
Recibe la imagen, tres valores booleanos si tiene convulsiones, si tiene pérdida visual y si tiene debilidad focal, el id del usuario que realizo la consulta y el id del medico al que se cargara
el diagnostico en su nombre.
Retorna un JSON con las probabilidades de cada clase. Las clases son las siguientes:
- Glioma
-Meningioma
- Pituitary
- No_tumor
Ademas guarda los datos de la consulta con su resultado en la base de datos.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/020488c5-9ba6-47a8-8a66-8181691f4324)

#### /Diagnosticos/predecir/pulmones [POST]

El objetivo de este endpoint es comunicarse con el modelo de pulmones para obtener las probabilidades de tener o no pulmonía.
Recibe la imagen, tres valores booleanos si tiene puntadas laterales, si tiene fiebre y si tiene dificultad respiratoria, el id del usuario que realizo la consulta y el id del medico al que se cargará
el diagnóstico en su nombre.
Retorna un JSON con las probabilidades de cada clase. Las clases son las siguientes:
- no_pneumonia
- pneumonia

Ademas guarda los datos de la consulta con su resultado en la base de datos.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/f7bc1b27-1c54-4d7b-88db-d0d592f8374d)

#### /Diagnosticos/predecir/corazon [POST]

El objetivo de este endpoint es comunicarse con el modelo de corazon para obtener las probabilidades de tener o no una enfermedad cardíaca.
Recibe la imagen, el id del usuario que realizo la consulta y el id del medico al que se cargará
el diagnóstico en su nombre.
Retorna un JSON con las predicciones.

Ademas guarda los datos de la consulta con su resultado en la base de datos.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/117873822/657d231f-468c-49eb-aca7-31a9937b59d5)




#### /Diagnosticos/historial [GET]

Obtiene el historial de diagnosticos. Si el que realiza la consulta es un auditor devuelve todos los diagnosticos guardados. Si es un medico devuelve los diagnosticos cargados a su nombre.
Recibe id de usuario y id de rol.
De cada diagnostico incluye la siguiente información:
- id
- imagen_id
- datos_complementarios
- fecha
- usuario_id
- usuario_medico_dni
- modelo_id
- nombre_usuario
- modelo_nombre
- nombre_medico
- imagen
- resultado

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/becfef2b-9888-49b5-a52e-7b576e4fc313)
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/bfb92b51-a293-49fa-b78a-3c6aaab69bce)


#### /Diagnosticos/{id_diagnostico} [GET]

Obtiene un diagnostico realizado a traves de su id.

Ejemplo de uso
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/25436270-3a5f-47c1-b936-a6f5d59f13c6)

#### /Diagnosticos/Delete/{id_diagnostico} [DELETE]

Elimina un diagnostico realizado a traves de su id.

Ejemplo de uso
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/a6abdd5d-081b-45c3-b065-dacbf6b6b46f)

### Usuarios

#### /Usuarios/medicos [GET]

Obtiene los usuario con rol de médico

Ejemplo de uso
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/c3ad6f1f-a191-4741-99cd-ab1c21a5f198)

#### /Usuarios/{id} [GET]

Obtiene el usuario por su id

Ejemplo de uso
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/0349c2dc-4b54-4172-8fc2-8423c7ce934a)

#### /Usuarios/admin/alta [POST]

Crea un usuario. Los datos que espera son:
  - "nombre": "string",
  - "dni": "string",
  - "email": "string",
  - "password": "string",
  - "rol_id": 0,
  - "establecimiento_id": 0,
  - "especialidad": "string"

Ejemplo de uso
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/b102f487-f263-4df9-aae3-fcd9d11664ce)

#### /Usuarios/update-user-informacion [PATCH]

Recibe un dni (requerido) y actualiza el usuario con ese dni para actuzalizar sus datos.
Recibe:
- dni (obligatorio)
- new_dni
- nombre
- password
- rol_id
- establecimiento_id
- escpecialidad
Solo mandar los datos que se deseen actualizar.
Por ejemplo si al usuario con dni "3534654" se le quiere actualizar el rol y la especialidad:

![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/1c476dbf-7621-4a2b-8b4e-bf8ace4c8adf)

#### /Usuarios/{dni}

Elimina un usuario mediante su dni
Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/299e09c6-4172-45d1-813e-aaca9b3e2986)







