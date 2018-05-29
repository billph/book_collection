from flask import Blueprint

bp = Blueprint("api", __name__)

from app.controllers.api import routes
