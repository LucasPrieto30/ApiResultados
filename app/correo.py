from flask_mail import Mail

mail = Mail()

def enviar_codigo_correo(correo, codigo):
    asunto = 'Código de Verificación'
    mensaje = f'Estimado usuario,\n\nHemos recibido una solicitud para acceder a su cuenta.\nTu código de verificación es: {codigo}\n\nSi no has solicitado este código, ignora este mensaje.'
    mail.send_message(subject=asunto, recipients=[correo], body=mensaje)