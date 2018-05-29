from flask import render_template, url_for, redirect, request, flash, jsonify, session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.controllers.social import bp
from app.models import User

@bp.route("/user/<username>", methods=["GET"])
@login_required
def user(username):
    u = User.query.filter_by(username=username).first_or_404()
    return render_template("social/user_page.html", user=u)

@bp.route("/addbio", methods=["POST"])
@login_required
def add_bio():
    data = request.get_json()
    if data["username"] != current_user.username:
        return redirect(url_for("errors.bad_request"))
    u = User.query.filter_by(username=data["username"]).first()
    u.bio = data["bio"]
    db.session.commit()
    return jsonify()
