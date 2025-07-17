from datetime import datetime
from . import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255))
    isbn = db.Column(db.String(100), unique=True)
    publisher = db.Column(db.String(255))
    pages = db.Column(db.Integer)
    stock = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<Book {self.title}>"

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    debt = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<Member {self.name}>"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    fee = db.Column(db.Float, default=0.0)

    book = db.relationship('Book', backref='transactions')
    member = db.relationship('Member', backref='transactions')

    def __repr__(self):
        return f"<Transaction BookID={self.book_id} MemberID={self.member_id}>"
