# ApiResultados
Api desarrollada en Flask para realizar conexion con el front y los modelos de machine learning.
Gestiona el acceso y manejo de usuarios, diagnosticos e historial.
Esta desarrollada en Flask-restx, lo que nos proporciona una interfaz Swagger para una documentacion interactiva de los metodos desarrollados.

La API se encuentra hosteada en Render y se puede acceder a traves del siguiente enlace
https://api-resultados.onrender.com

## Endpoints

### Diagnosticos

En esta sección se encuentran los endpoints que manejan los diagnosticos, resultados e historial. Para realizar los diagnosticos/predicciones se conecta con APIS desarrolladas por los equipos de los modelos.

#### /Diagnosticos/predecir/cerebro [POST]

El objetivo de este endpoint es comunicarse con el modelo del cerebro para obtener las probabilidades de los siguientes diagnósticos relacionados al cerebro: Glioma, Meningioma, Pituitary y No tumor.

Recibe como parámetros la imagen, datos complementarios (perdida visual, debilidad focal y convulsiones), el id del usuario que realizo la consulta, el id del medico al que se cargará
el diagnóstico en su nombre y los datos del paciente como la fecha de nacimiento, peso, altura y sexo.
Retorna un JSON con las probabilidades de cada diagnóstico junto al id de imagen e id del diagnóstico.

Ademas guarda los datos de la consulta con su resultado en la base de datos.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/117873822/5226e21f-c4e7-4ebf-acf2-98b7f15876ec)


#### /Diagnosticos/predecir/pulmones [POST]

El objetivo de este endpoint es comunicarse con el modelo de pulmones para obtener las probabilidades de los siguientes diagnósticos relacionados al pulmón: Neumonía y No neumonía

Recibe como parámetros la imagen, datos complementarios (puntada lateral, fiebre y dificultad respiratoria), el id del usuario que realizo la consulta, el id del medico al que se cargará el diagnóstico en su nombre y los datos del paciente como la fecha de nacimiento, peso, altura y sexo.
Retorna un JSON con las probabilidades de cada diagnóstico junto al id de imagen e id del diagnóstico.

Ademas guarda los datos de la consulta con su resultado en la base de datos.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/f7bc1b27-1c54-4d7b-88db-d0d592f8374d)

#### /Diagnosticos/predecir/corazon [POST]

El objetivo de este endpoint es comunicarse con el modelo del corazón para obtener las probabilidades de los siguientes diagnósticos relacionados al corazón: Contracción ventricular, Fusión Ventricular Normal, Infarto, No clasificable, Normal y Prematuro Supraventricular.

Recibe como parámetros la imagen, datos complementarios (palpitaciones, dolor superior izquierdo y disnea), el id del usuario que realizo la consulta, el id del medico al que se cargará
el diagnóstico en su nombre y los datos del paciente como la fecha de nacimiento, peso, altura y sexo.
Retorna un JSON con las probabilidades de cada diagnóstico junto al id de imagen e id del diagnóstico.

Ademas guarda los datos de la consulta con su resultado en la base de datos.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/117873822/d105f6fb-c316-442e-8c42-7d6198e42132)


#### /Diagnosticos/predecir/muñeca [POST]

El objetivo de este endpoint es comunicarse con el modelo de muñeca para obtener las probabilidades de los siguientes diagnósticos relacionados a la muñeca: Fractura y Sano.

Recibe como parámetros la imagen, datos complementarios (dolor con limitación, edema y deformidad), el id del usuario que realizo la consulta, el id del medico al que se cargará
el diagnóstico en su nombre y los datos del paciente como la fecha de nacimiento, peso, altura y sexo.
Retorna un JSON con las probabilidades de cada diagnóstico junto al id de imagen e id del diagnóstico.

Ademas guarda los datos de la consulta con su resultado en la base de datos.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/117873822/9f532304-0522-4c21-874f-f74bd6ae4d9b)


#### /Diagnosticos/predecir/riñones [POST]

El objetivo de este endpoint es comunicarse con el modelo de riñones para obtener las probabilidades de los siguientes diagnósticos relacionados al riñón: Normal, Piedra, Quiste y Tumor. 

Recibe como parámetros la imagen, datos complementarios (hermaturia, dolor lumbar, dolor abdominal, fiebre y perdida de peso), el id del usuario que realizo la consulta, el id del medico al que se cargará el diagnóstico en su nombre y los datos del paciente como la fecha de nacimiento, peso, altura y sexo.
Retorna un JSON con las probabilidades de los cuatro diagnosticos mencionados anteriormente junto al id de imagen e id del diagnóstico.

Ademas guarda los datos de la consulta con su resultado en la base de datos.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/117873822/eccc9965-36f5-43bb-bc83-5604c9698a50)

#### /Diagnosticos/predecir/rodilla [POST]

El objetivo de este endpoint es comunicarse con el modelo de rodilla para obtener las probabilidades de los siguientes diagnósticos relacionados al ligamento cruzado anterior(LCA): LCA Sano y Rotura LCA 
Recibe como parámetros la imagen, datos complementarios (inestabilidad, cajón anterior positivo e impotencia funcional), el id del usuario que realizo la consulta, el id del medico al que se cargará el diagnóstico en su nombre y los datos del paciente como la fecha de nacimiento, peso, altura y sexo.
Retorna un JSON con las probabilidades de los diagnosticos mencionados anteriormente junto al id de imagen e id del diagnóstico.

Ademas guarda los datos de la consulta con su resultado en la base de datos.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/117873822/93a04725-6f08-424e-a5cb-121d93ed076c)

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
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/839b3941-d531-4f59-9d87-88c6c810f209)
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/57924e0c-6b33-49be-84dc-b2f281030593)

#### /Diagnosticos/Delete/{id_diagnostico} [DELETE]

Elimina un diagnostico realizado a traves de su id.

Ejemplo de uso
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/a6abdd5d-081b-45c3-b065-dacbf6b6b46f)

### Usuarios

#### /Usuarios/login [POST]
Realiza el login de un usuario mediante su dni y contraseña. Si el usuario es Auditor o Administrador se le envía un código por mail para realizar la verificación doble.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/d95d697a-d3c4-44a1-91e4-2d9bdb919535)


#### /Usuarios/registro [POST]

Crea un usuario. Los datos que espera son:
  - "nombre": "string",
  - "apellido: "string",
  - "dni": "string",
  - "email": "string",
  - "password": "string",
  - "rol_id": int,
  - "establecimiento_id": int,
  - "especialidad": "string"

Ejemplo de uso
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/230e89f6-520d-4861-babb-4d7b981d61fc)


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

#### /Usuarios/reset_pass/{dni} [POST]
Recibe un dni y envía al usuario un codigo por mail para que pueda resetear su contraseña.

#### /Usuarios/check_code [POST]
Recibe el codigo para resetear la contraseña y verifica si es válido.

#### /Usuarios/reset_password [POST]
Recibe la nueva contraseña del usuario y luego la guarda en la base de datos.

#### /Usuarios/verificacion [POST]
Este endpoint se utiliza para verificar la identidad del usuario antes de permitirle acceder a ciertos recursos de la aplicación.
Recibe el dni del usuario y un codigo OTP (One Time Password) y luego verifica si el código es válido.

#### /Usuarios/medicos [GET]

Obtiene los usuario con rol de médico

Ejemplo de uso
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/c3ad6f1f-a191-4741-99cd-ab1c21a5f198)

#### /Usuarios/contacto [POST]
Recibe el nombre, apellido, email del usuario y el mensaje y lo guarda en la base de datos.

#### /Usuarios/establecimientos [GET]
Obtiene todos los establecimientos médicos registrados en el sistema.

Ejemplo de uso
![image](https://github.com/LucasPrieto30/ApiResultados/assets/117873822/1dd67fda-167b-4d5f-a12a-93bfc4607863)

#### /Usuarios/{id} [GET]

Obtiene el usuario por su id

Ejemplo de uso
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/0349c2dc-4b54-4172-8fc2-8423c7ce934a)


#### /Usuarios/{dni}

Elimina un usuario mediante su dni

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/299e09c6-4172-45d1-813e-aaca9b3e2986)


### Feedback

#### /Feedback/cerebro
Realiza el feedback al modelo de cerebro. Se debe enviar el id de la imagen del diagnostico, una de las etiquetas (glioma, meningioma, pituitary ó no_tumor) en "true" y un comentario.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/95fa3685-37ac-446e-a8d2-34409876fd9c)


#### /Feedback/pulmones
Realiza el feedback al modelo de pulmones. Se debe enviar el id de la imagen del diagnostico, una de las etiquetas (pneumonia ó no_pneumonia) en "true" y un comentario.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/66337029/6e5ce919-16b0-4cc1-b9d7-97f153dcb41c)

#### /Feedback/corazon
Realiza el feedback al modelo de corazón. Se debe enviar el id de la imagen del diagnostico, una de las etiquetas (contraccion_ventricular_prematura, latido_normal, fusion_de_latido_ventricular_y_normal, infarto_de_miocardio, latido_no_clasificable ó latido_prematuro_supraventricular) en "true" y un comentario.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/117873822/34bc0376-652f-4227-b153-e4428c9baa93)

#### /Feedback/muñeca
Realiza el feedback al modelo de fractura de muñeca. Se debe enviar el id de la imagen del diagnostico, una de las etiquetas (contraccion_ventricular_prematura, latido_normal, fusion_de_latido_ventricular_y_normal, infarto_de_miocardio, latido_no_clasificable ó latido_prematuro_supraventricular) en "true" y un comentario.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/117873822/5a0d2cab-4ad8-4db7-9724-41c3f6ed04cb)

#### /Feedback/riñones
Realiza el feedback al modelo de riñones. Se debe enviar el id de la imagen del diagnostico, una de las etiquetas (quiste, tumor, piedra ó normal) en "true" y un comentario.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/117873822/0b90ef70-27c9-4d16-b2e6-3dcd59a370d9)

#### /Feedback/rodilla
Realiza el feedback al modelo de rodilla. Se debe enviar el id de la imagen del diagnostico, una de las etiquetas (rotura_lca ó lca_sano) en "true" y un comentario.

Ejemplo de uso:
![image](https://github.com/LucasPrieto30/ApiResultados/assets/117873822/e9c4cf96-46f4-46ef-9589-b368b185aae0)

