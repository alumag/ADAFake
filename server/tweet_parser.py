import re

import tweepy
from apikey import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

pattern = "https://twitter.com/\w+/status/(\d+)"
compiled = re.compile(pattern=pattern)


def get_tweet(url):
    tweet_id = compiled.findall(url)
    if not tweet_id:
        raise ValueError()
    tweet_id = tweet_id[0]

    return api.get_status(tweet_id)._json

