from flask import render_template, url_for, redirect, request, flash
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app.controllers.auth import bp
from app.models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return "You are already logged in"
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')

        if len(password) <= 8 and len(username) < 1:
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))

        login_user(user, remember=bool(remember))
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return "You are already logged in"
    if request.method == "POST":
        pass
    return render_template("auth/register.html")
