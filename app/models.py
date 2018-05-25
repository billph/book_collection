from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User_Book(db.Model):
    __tablename__ = "user_book"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    book_id = db.Column(db.String(15), db.ForeignKey("book.id"), primary_key=True)
    finished = db.Column(db.Boolean)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(1000))
    topics = db.Column(db.String(1000))


class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(80), unique=True, nullable=False)
    preferences = db.Column(db.String(100))
    books = db.relationship("Book", secondary="user_book", lazy='dynamic')

    def add_book(self, book):
        self.books.append(book)
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

class Book(db.Model):
    __tablename__ = "book"
    
    id = db.Column(db.String(15), primary_key=True)
    book_name = db.Column(db.String(200))
    genre = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(300), nullable=False)
    users = db.relationship("User", secondary="user_book", lazy='dynamic')

    def __repr__(self):
        return "<Book {}>".format(self.book_name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    