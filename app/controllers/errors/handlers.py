import os
from flask import render_template, abort

from app import db
from app.controllers.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500

@bp.route("/badrequest400")
def bad_request():
    return abort(400)
