from flask import Flask
from .extensions import api
from .pruebas import ns, ns2
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    api.init_app(app)

    api.add_namespace(ns)
    api.add_namespace(ns2)
    CORS(app)

    return app