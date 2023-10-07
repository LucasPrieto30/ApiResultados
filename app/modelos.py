from flask_restx import fields
from .extensions import api

post_model = api.model("PostImagen", {
    "img": fields.String
})
pacienteDiagnostico = api.model("pacienteDiagnostico", {
    "UsuarioId": fields.String,
    "Edad": fields.Integer,
    "Peso": fields.Float,
    "AlturaCM": fields.Float,
    "Sexo": fields.String,
    "SeccionCuerpo": fields.String,
    "CondicionesPrevias": fields.String,
    "Imagen": fields.String
})