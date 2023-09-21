from flask_restx import fields
from .extensions import api

post_model = api.model("Post", {
    "img": fields.String
})