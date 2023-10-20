import base64
import io
from PIL import Image 
import requests

url = 'http://127.0.0.1:5000/Diagnosticos/84' 

response = requests.get(url)

print(response.status_code)
json_respuesta = response.json()

# extraer los datos binarios codificados en base64 
datos_binarios_base64 = json_respuesta['imagen']

# decodificar los datos binarios base64
datos_binarios = base64.b64decode(datos_binarios_base64)

# crear una imagen a partir de los datos binarios
imagen = Image.open(io.BytesIO(datos_binarios))

# mostrar la imagen
imagen.show()