import re
from flask import render_template, url_for, redirect, request, flash, jsonify, session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.controllers.api import bp
from app.models import User, Book

@bp.route("/userexist", methods=["POST"])
def user_exist():
    username = request.get_json()
    if username["username"]:
        if User.query.filter_by(username=username["username"]).first() is None:
            return jsonify({"usable": "true"}) 
    return jsonify({"usable": "false"})  

@bp.route("/flash_message", methods=["POST"])
@login_required
def flash_message():
    try:
        message = request.get_json()
        if message["message"]:
            flash(message["message"])
    except KeyError:
        return redirect(url_for("errors.bad_request"))
    return jsonify()

@bp.route("/addbook", methods=["POST"])
@login_required
def add_book_by_isbn():
    print(current_user.username)
    try:
        data = request.get_json()
        isbn = str(data["isbn"])
        if len(isbn) != 10 and len(isbn) != 13:
            return redirect(url_for("errors.bad_request"))
        book = Book.query.filter_by(id=isbn).first()
        if not book:
            book = Book(id=str(isbn))
            db.session.add(book)
            db.session.commit()
            book = Book.query.filter_by(id=isbn).first()
        current_user.add_book(book)
    except KeyError:
        return redirect(url_for("errors.bad_request"))
    return jsonify()

@bp.route("/getbooks", methods=["POST"])
@login_required
def get_books():
    try:
        data = request.get_json()
        username = data["username"]
        print(username)
        user = User.query.filter_by(username=username).first()
        print(user)
        if not user:
            return redirect(url_for("errors.bad_request"))
        list_of_books = user.get_books()
        return jsonify({"value": list_of_books})
    except KeyError:
        return redirect(url_for("errors.bad_request"))
    return jsonify()



