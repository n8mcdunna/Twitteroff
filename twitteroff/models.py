"""SQLAlchemy models and utility functions"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    """Twitter user table that will correspond to tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<User: {}>".format(self.name)

class Tweet(DB.Model):
    """Tweet text data that is associated with User table"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.String)
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, 
                        DB.ForeignKey("user.id"), 
                        nullable=False)
    user = DB.relationship(
        'User', 
        backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)

