import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_jsglue import JSGlue
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Please login to access this page"
cors = CORS()
jsglue = JSGlue()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder=config_class.TEMPLATE_URL, static_folder=config_class.STATIC_URL)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    cors.init_app(app)
    jsglue.init_app(app)

    from app.controllers.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.controllers.api import bp as api_bp
    app.register_blueprint(api_bp)

    from app.controllers.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.controllers.social import bp as social_bp
    app.register_blueprint(social_bp)

    return app

from app import models
