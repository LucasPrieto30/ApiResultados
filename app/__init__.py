from flask import Flask
from .extensions import api
from .diagnosticos import ns, ns2, feedbackNs
from .usuarios import ns_usuarios
from flask_cors import CORS
from .correo import mail
from database.dto_medico import obtener_clave_desde_Medico
from flask_restx import Api
def create_app():
    app = Flask(__name__)
    api = Api(app, security='jwt', authorizations={'jwt': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}})
    app.config['SECRET_KEY'] = obtener_clave_desde_Medico()
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'datacript2023@gmail.com'
    app.config['MAIL_PASSWORD'] = 'pjgm mzqp hupq buln'
    app.config['MAIL_DEFAULT_SENDER'] = ('Datacript','datacript2023@gmail.com')
    mail.init_app(app)
    
    #api.init_app(app)

    api.add_namespace(ns)
    api.add_namespace(ns2)
    api.add_namespace(ns_usuarios)
    api.add_namespace(feedbackNs)
    CORS(app,supports_credentials=True)

    return app