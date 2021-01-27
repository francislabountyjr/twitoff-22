"""Retrieve Tweets, embeddings, and put them in our Database"""

from os import getenv
import tweepy  # Allows interaction with Twitter
import spacy  # Vectorizes tweets
from .models import DB, Tweet, User


TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")

TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load('my_model')


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    try:
        # Create user based on the username passed into the function
        twitter_user = TWITTER.get_user(username)
        # If they exist in local db, update that user
        # Else get user from Twitter db and insantiate a new user
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)

        # Add the user to our database
        DB.session.add(db_user)

        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode='Extended'
        )  # A list of tweets from 'username'

        # empty tweets list == false
        if tweets:
            # update newest tweet id
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            # For each tweet create an embedding
            vectorized_tweet = vectorize_tweet(tweet.text)
            # Create tweet that will be added to our DB
            db_tweet = Tweet(id=tweet.id, text=tweet.text,
                             vect=vectorized_tweet)
            # Append each tweet from 'username' to username.tweets
            db_user.tweets.append(db_tweet)
            # Add db_tweet to Tweet database
            DB.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else:
        # Commit everything to the database
        DB.session.commit()


def insert_example_users():
    add_or_update_user('joebiden')
