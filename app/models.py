from datetime import datetime
import os
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from operator import itemgetter

class User_Book(db.Model):
    __tablename__ = "user_book"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    book_id = db.Column(db.String(15), db.ForeignKey("book.id"), primary_key=True)
    finished = db.Column(db.Boolean)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(1000))
    topics = db.Column(db.String(1000))
    title = db.Column(db.String(100))
    authors = db.Column(db.String(50))
    pages = db.Column(db.Integer)

class Friendship(db.Model):
    __tablename__ = "friend"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


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
    first_book = db.Column(db.DateTime)
    first_join = db.Column(db.DateTime, default=datetime.utcnow)
    first_following = db.Column(db.DateTime)
    first_ten_books = db.Column(db.DateTime)
    first_unfollow = db.Column(db.DateTime)
    first_bio = db.Column(db.DateTime)

    followers = db.relationship('Friendship', backref='to', primaryjoin=id==Friendship.following_id)
    following = db.relationship('Friendship', backref='from', primaryjoin=id==Friendship.user_id)

    def add_avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def add_bio(self, bio):
        self.bio = bio
        if not self.first_bio:
            self.first_bio = datetime.utcnow()
        db.session.commit()

    def get_activities(self):
        list_of_activites = [
            {
                "name": "First Book",
                "date": self.first_book
            }, 
            {
                "name": "join The Book",
                "date": self.first_join
            }, 
            {
                "name": "First Bio",
                "date": self.first_following
            },
            {   "name": "First Ten Books",
                "date": self.first_ten_books
            },
            {
                "name": "First Bio",
                "date": self.first_bio
            }
        ]

        avail_activities = [i for i in list_of_activites if i["date"]]
        avail_activities.sort(key=itemgetter("date"), reverse=True)

        return avail_activities
        

    def follow(self, user):
        if not self.is_following(user):
            f = Friendship(user_id=self.id, following_id=user.id)
            db.session.add(f)
            if not self.first_following:
                self.first_following = datetime.utcnow()
            db.session.commit()

    def change_finish(self, book_user):
        book_user.finished = not book_user.finished
        db.session.commit()

    
    def unfollow(self, user):
        if self.is_following(user):
            Friendship.query.filter_by(user_id=self.id, following_id=user.id).delete()
            if not self.first_unfollow:
                self.first_unfollow = datetime.utcnow()

            db.session.commit()
            
    def is_following(self, user):
        return Friendship.query.filter_by(user_id=self.id, following_id=user.id).count() > 0

    def get_followers(self):
        return self.following_users.filter(following.c.user_id == self.id).all()

    def add_book(self, book, title, authors, pages):
        exist = self.books.filter_by(id=book.id).first()
        if not exist:
            user_book = User_Book(user_id=self.id, book_id=book.id, finished=False, title=title, authors=authors, pages=pages)
            db.session.add(user_book)
            if not self.first_book:
                self.first_book = datetime.utcnow()
            elif not self.first_ten_books:
                if len(self.get_books()) == 10:
                    self.first_ten_books = datetime.utcnow()

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
