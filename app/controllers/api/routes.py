import re
from flask import render_template, url_for, redirect, request, flash, jsonify, session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.controllers.api import bp
from app.models import User, Book, User_Book

# check if username is existed. Needs username as data
@bp.route("/userexist", methods=["POST"])
def user_exist():
    username = request.get_json()
    if username["username"]:
        if User.query.filter_by(username=username["username"]).first() is None:
            return jsonify({"usable": "true"}) 
    return jsonify({"usable": "false"})  

# flashed message API. Take in a message then it would put a flash in the stack
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

# take in the isbn of the book
@bp.route("/addbook", methods=["POST"])
@login_required
def add_book_by_isbn():
    try:
        data = request.get_json()
        isbn = str(data["isbn"])
        authors = str(data["authors"])
        pages = str(data["pages"])
        title = str(data["title"])
        if len(isbn) != 10 and len(isbn) != 13:
            return redirect(url_for("errors.bad_request"))
        book = Book.query.filter_by(id=isbn).first()
        if not book:
            book = Book(id=str(isbn))
            db.session.add(book)
            db.session.commit()
            book = Book.query.filter_by(id=isbn).first()
        book_exist = User_Book.query.filter_by(user_id=current_user.id, book_id=isbn).first()
        if book_exist:
            User_Book.query.filter_by(user_id=current_user.id, book_id=isbn).delete()
            db.session.commit()
            return jsonify({"success": True, "delete": True})
        else:
            current_user.add_book(book, authors=authors, pages=pages, title=title)
    except KeyError:
        return redirect(url_for("errors.bad_request"))
    return jsonify({"success": True, "delete": False})

# get a list of all books user have
@bp.route("/getbooks", methods=["POST"])
@login_required
def get_books():
    try:
        data = request.get_json()
        username = data["username"]
        user = User.query.filter_by(username=username).first()
        if not user:
            return redirect(url_for("errors.bad_request"))
        list_of_books = user.get_books()
        return jsonify({"value": list_of_books})
    except KeyError:
        return redirect(url_for("errors.bad_request"))
    return jsonify()

# check if a book is owned by a specific user
@bp.route("/hasbook", methods=["POST"])
@login_required
def has_book():
    try:
        data = request.get_json()
        isbn = data["isbn"]
        book = Book.query.filter_by(id=isbn).first()
        if not book:
            return jsonify({"has": False})
        return jsonify({"has": (isbn in current_user.get_books())})
    except KeyError:
        return redirect(url_for("errors.bad_request"))

# change the status of finishign the book of a user
@bp.route("/changefinish", methods=["POST"])
@login_required
def change_finish():
    try:
        data = request.get_json()
        isbn = data["isbn"]
        book = Book.query.filter_by(id=isbn).first()
        if not book:
            return redirect(url_for("errors.bad_request"))
        user_book = User_Book.query.filter_by(user_id=current_user.id, book_id=book.id).first()
        if not user_book:
            return redirect(url_for("errors.bad_request"))
        current_user.change_finish(user_book)
        return jsonify({"success": True, "finished": user_book.finished})
    except KeyError:
        return redirect(url_for("errors.bad_request"))
