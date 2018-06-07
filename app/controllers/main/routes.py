from flask import render_template, url_for, redirect, request, flash, jsonify, session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.controllers.main import bp
from app.models import User, User_Book

# Main route. This route is the homepage when once user logs in
@bp.route("/")
@login_required
def home():
    books = User_Book.query.filter_by(user_id=current_user.id).all()
    return render_template("main/home.html", books=books, home=True, title="Dashboard")