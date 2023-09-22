from flask import Flask
from .extensions import api
from .pruebas import ns
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    api.init_app(app)

    api.add_namespace(ns)

    return app