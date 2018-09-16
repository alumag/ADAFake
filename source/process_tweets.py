import numpy as np
import pandas as pd
import scipy
from gensim.models import Word2Vec
# todo - add to requirements !
from textblob import TextBlob
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction import text
import pickle as pkl

MAX_BOW=40
MAX_WRD2VEC=10


def process_train_text(txt):
    tknzr = TweetTokenizer()
    sentiments = []
    for wrd in txt:
        sentiments.append(TextBlob(wrd).sentiment)
    vectorizer = text.TfidfVectorizer(max_features=MAX_BOW, max_df=0.05, tokenizer=tknzr.tokenize, analyzer='word')
    vectorizer.fit(txt)
    txt = vectorizer.transform(txt)
    with open("../data/vectorizer.pkl", 'wb') as f:
        pkl.dump(vectorizer, f)
    return scipy.sparse.hstack([txt, np.array(sentiments)])


def process_test_text(txt):
    sentiments = []
    for wrd in txt:
        sentiments.append(TextBlob(wrd).sentiment)
    vectorizer = pkl.load(open("../data/vectorizer.pkl",'rb'))
    txt = vectorizer.transform(txt)
    return scipy.sparse.hstack([txt, np.array(sentiments)])


def get_text_features(textual_data,isTrain):
    # features for tweet body
    total = textual_data[:,0] + textual_data[:,1]
    if isTrain:
        txt_emb = process_train_text(total)
    else:
        txt_emb = process_test_text(total)

    # text_features = scipy.sparse.hstack([author_emb, txt_emb])
    return txt_emb


COL_NUM_NAMES = ["retweet_count","user_verified","user_friends_count","user_followers_count","user_favourites_count","num_hashtags","num_mentions"]


def get_features(tweet_data,isTrain=False):
    numeric_data = tweet_data[COL_NUM_NAMES]
    numeric_data["user_verified"] = numeric_data["user_verified"].astype(int)
    textual_data = tweet_data[['text', 'user_screen_name']].values
    textual_data = get_text_features(textual_data,isTrain)
    return np.hstack([np.asarray(scipy.sparse.csr_matrix.todense(textual_data)),numeric_data.values])


# read dataset
def get_train_data(path="../data/electionday_tweets_clean.xlsx"):
    original_data = pd.read_excel(path, header=0)
    labels = original_data["is_fake_news"].astype(int).values
    processed_data = get_features(original_data[['text', 'user_screen_name'] + COL_NUM_NAMES],True)
    return processed_data, labels


if __name__ == "__main__":
    processed_data, labels = get_train_data()
    with open("../data/processed_data.pkl",'wb') as f:
        pkl.dump([processed_data, labels], f)
