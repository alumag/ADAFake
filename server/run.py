import flask
from flask import request, jsonify

from tweet_parser import get_tweet
from source.ADAFakeDetector import check_tweet as ADAFakeDetector_checkTweet

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>ADA Fake News Detector</h1>"


@app.route('/api/v1/checkTweet', methods=['GET'])
def check_twit():
    response = dict()

    url = request.args['url']
    response["url"] = url

    tweet_data = get_tweet(url)

    response["fake_news"] = ADAFakeDetector_checkTweet(tweet_data)

    return jsonify(response)


app.run()
