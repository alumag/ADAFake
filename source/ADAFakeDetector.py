import pandas
from .model import evaluate
from .process_tweets import get_features, COL_NUM_NAMES


def check_tweet(tweet_data):
    """"
    :return True on fake news, false on true once
    """
    tweet_data = pandas.DataFrame(tweet_data)
    processed_data = get_features(tweet_data[['text', 'user_screen_name'] + COL_NUM_NAMES])
    return evaluate(processed_data)
