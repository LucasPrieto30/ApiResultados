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
Recibe la imagen, tres valores booleanos si tiene epilepsia, si tiene problemas visuales y si tiene decadencia motriz, el id del usuario que realizo la consulta y el id del medico al que se cargara
el diagnostico en su nombre.
Retorna un JSON con las probabilidades de cada clase. Las clases son las siguientes:
- Glioma
-Meningioma
- Pituitary
- No_tumor
Ademas guarda los datos de la consulta con su resultado en la base de datos.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/31454195-48b4-463f-9106-85db699b34ab)

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


#### /Diagnosticos/historial [GET]

Obtiene el historial de diagnosticos. Si el que realiza la consulta es un auditor devuelve todos los diagnosticos guardados. Si es un medico devuelve los diagnosticos cargados a su nombre.
Recibe id de usuario y id de rol.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/3e7252eb-fce7-42de-90c4-24eee6a2ca12)

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
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/3906373d-4ae3-4a52-9fcc-cc9c020fb24f)


#### /Usuarios [POST]

Crea un usuario. Los datos que espera por body son:
{
  - "nombre": "string",
  - "dni": "string",
  - "email": "string",
  - "password": "string",
  - "rol_id": 0,
  - "establecimiento_id": 0,
  - "fecha_ultima_password": "2023-10-20T18:46:01.327Z",
  - "especialidad": "string"
}

Ejemplo de uso

![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/0b3408c0-ab18-4a42-b403-801280f43084)


