from datetime import datetime
import os
from hashlib import md5
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
    password = db.Column(db.String(128))
    email = db.Column(db.String(80), nullable=False)
    preferences = db.Column(db.String(100))
    bio = db.Column(db.String(60))
    books = db.relationship("Book", secondary="user_book", lazy='dynamic')

    def add_avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def add_book(self, book):
        exist = self.books.filter_by(id=book.id).first()
        if not exist:
            user_book = User_Book(user_id=self.id, book_id=book.id, finished=False)
            db.session.add(user_book)
            db.session.commit()

    def get_books(self):
        list_of_isbn = []
        for i in self.books.all():
            list_of_isbn.append(str(i.id))
        return list_of_isbn

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

class Book(db.Model):
    __tablename__ = "book"
    
    id = db.Column(db.String(15), primary_key=True)
    users = db.relationship("User", secondary="user_book", lazy='dynamic')

    def __repr__(self):
        return "<Book {}>".format(self.id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    