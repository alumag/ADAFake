### Usage
1) Add `apikey.py` to the directory including your twitter api credentials
````python
ACCESS_TOKEN = '*******'
ACCESS_SECRET = '*******'
CONSUMER_KEY = '*******'
CONSUMER_SECRET = '*******'
````

2) Run the server `./run.py`

The server run on `127.0.0.1:5000` and accept api requests using `http://127.0.0.1:5000/api/v1/checkTweet?url={tweet-url}`