import re

import tweepy
from apikey import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

pattern = "https://twitter.com/\w+/status/(\d+)"
compiled = re.compile(pattern=pattern)


def get_relevant_tweet_data(tweet):
    relevant_data = dict(
        tweet_id=tweet["id"],
        created_at=tweet["created_at"],
        retweet_count=tweet["retweet_count"],
        text=tweet["text"],
        user_screen_name=tweet["user"]["screen_name"],
        user_verified=tweet["user"]["verified"],
        user_friends_count=tweet["user"]["friends_count"],
        user_followers_count=tweet["user"]["followers_count"],
        user_favourites_count=tweet["user"]["favourites_count"],
        num_hashtags=len(tweet["entities"]["hashtags"]),
        num_mentions=len(tweet["entities"]["user_mentions"]),
        num_urls=len(tweet["entities"]["urls"])
    )

    return relevant_data


def get_tweet(url):
    tweet_id = compiled.findall(url)
    if not tweet_id:
        raise ValueError()
    tweet_id = tweet_id[0]
    tweet = api.get_status(tweet_id)._json

    return get_relevant_tweet_data(tweet)

