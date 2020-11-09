"""SQLAlchemy models and utility functions"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    """Twitter user table that will correspond to tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "<User: {}>".format(self.name)

class Tweet(DB.Model):
    """Tweet text data that is associated with User table"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)

def insert_example_users():
    nate = User(id=1, name="Nate")
    mae = User(id=2, name="Maegan")
    DB.session.add(nate)
    DB.session.add(mae)
    DB.session.commit()
