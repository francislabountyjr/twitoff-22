"""SQLAlchemy models and utility functions for twitoff"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# User Table
class User(DB.Model):
    """Twitter Users corresponding to Tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)  # id column
    name = DB.Column(DB.String, nullable=False)  # name column
    newest_tweet_id = DB.Column(DB.BigInteger)  # newest_tweet_id column

    def __repr__(self):
        return '<User: {}>'.format(self.name)


# Tweet Table
class Tweet(DB.Model):
    """Tweets corresponding to Users"""
    id = DB.Column(DB.BigInteger, primary_key=True)  # id column
    text = DB.Column(DB.Unicode(300))  # tweet text column
    vect = DB.Column(DB.PickleType, nullable=False)  # vectorized tweet column
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)  # foreign key to link to User table
    # set up relationship between User table and Tweet table
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet: {}>'.format(self.text)
