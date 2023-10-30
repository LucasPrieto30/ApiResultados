from flask import Flask
from .extensions import api
from .diagnosticos import ns, ns2, feedbackNs
from .usuarios import ns_usuarios
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    api.init_app(app)

    api.add_namespace(ns)
    api.add_namespace(ns2)
    api.add_namespace(ns_usuarios)
    api.add_namespace(feedbackNs)
    CORS(app)

    return app