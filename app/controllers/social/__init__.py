from flask import Blueprint

bp = Blueprint("social", __name__)

from app.controllers.social import routes
