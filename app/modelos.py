from flask_restx import fields
from .extensions import api

post_model = api.model("Post1", {
    "img": fields.String
})
post_model1 = api.model("Post2", {
    "ID_user": fields.String,
    "Edad": fields.Integer,
    "Peso": fields.Float,
    "Altura cm": fields.Float,
    "Sexo": fields.String,
    "Sección del cuerpo": fields.String,
    "condiciones previas": fields.String,
    "Imagen": fields.String
})