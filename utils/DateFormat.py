import datetime

class DateFormat():
    
    @classmethod
    def convert_time(self, date):
        return datetime.datetime.strftime(date, "%d/%m/%Y")
    
    @classmethod
    def extraer_horas(self, time):
        return time.strftime("%H:%M")