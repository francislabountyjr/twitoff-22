"""Prediction of Users based on Tweet Embeddings"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Determine who is more likely to have made a hypothetical tweet
    """
    user0 = User.query.filter(User.name == user0_name).one()  # user0
    user1 = User.query.filter(User.name == user1_name).one()  # user1

    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Vertically stack embeddings to create one list of vects
    vects = np.vstack([user0_vects, user1_vects])  # user0_vects on user1_vects

    # Collection of labels same length as vects
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)),
         np.ones(len(user1.tweets))]
    )  # 0 is user0, 1 is user1

    # Create logistic regression model and fit
    log_reg = LogisticRegression().fit(vects, labels)

    # Reassign passed in variable to vectorized version
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # Format hypo_tweet_vect and run predictions, will return 0 or 1
    return log_reg.predict(np.array(hypo_tweet_vect).reshape(1, -1))
