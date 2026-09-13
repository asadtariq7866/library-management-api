from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    copies_total = db.Column(db.Integer, nullable=False)
    copies_available = db.Column(db.Integer, nullable=False)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    joined_date = db.Column(db.Date, default=date.today)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    borrowed_date = db.Column(db.Date, default=date.today)
    due_date = db.Column(db.Date, nullable=False)
    returned_date = db.Column(db.Date, nullable=True)

    book = db.relationship('Book', backref='loans')
    member = db.relationship('Member', backref='loans')