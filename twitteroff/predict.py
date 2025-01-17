import numpy as np 
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet

def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Predict which user says hypothetical tweet.
    Returns 0 for user0 or 1 for user1
    """
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    vects = np.vstack([user0_vects, user1_vects])

    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))]
        )
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    log_reg = LogisticRegression().fit(vects, labels)
    
    return log_reg.predict(hypo_tweet_vect.reshape(1, -1))