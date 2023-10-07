from utils.DateFormat import DateFormat

class Historial():
    
    def __init__(self,id, fecha=None, hora=None, estudio=None,descripcion=None) -> None:
        self.id=id
        self.fecha=fecha
        self.hora=hora
        self.estudio=estudio
        self.descripcion=descripcion

    def to_JSON(self):
        return  {
            'id': self.id,
            'fecha': DateFormat.convert_time(self.fecha),
            'hora': DateFormat.extraer_horas(self.hora),
            'estudio': self.estudio,
            'descripcion': self.descripcion
        }
    