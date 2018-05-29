import re
from flask import render_template, url_for, redirect, request, flash, jsonify, session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.controllers.auth import bp
from app.models import User

@bp.route("/userexist", methods=["POST"])
def user_exist():
    username = request.get_json()
    if username["username"]:
        if User.query.filter_by(username=username["username"]).first() is None:
            return jsonify({"usable": "true"}) 
    return jsonify({"usable": "false"})       


