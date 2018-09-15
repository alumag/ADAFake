import numpy as np
import pandas as pd
from gensim.models import Word2Vec
# todo - add to requirements !
from textblob import TextBlob
from nltk.tokenize import TweetTokenizer
from collections import Counter


def process_author_name(txt):
    model = Word2Vec(sentences=list(txt),  # tokenized senteces, list of list of strings
             size=10,  # size of embedding vectors
             min_count=20,  # minimum frequency per token, filtering rare words
             sample=0.05,  # weight of downsampling common words
             sg=0,  # should we use skip-gram? if 0, then cbow
             iter=5,
             hs=0)
    return model[model.wv.vocab]

def process_text(txt):
    tknzr = TweetTokenizer()
    bow = Counter(tknzr.tokenize(txt))
    sentiments = []
    for str in txt:
       sentiments.append(TextBlob(str).sentiment)




def get_text_features(textual_data):
    # word2vec for usernames
    author_emb = process_author_name(textual_data[:,1])
    # features for tweet body
    txt_emb = process_text(textual_data[:,2])
    tezt_feat = np.vstack([author_emb, txt_emb])
    return tezt_feat



def get_features(tweet_data):
    numeric_data = tweet_data[["retweet_count","user_verified","user_friends_count","user_followers_count","user_favourites_count","num_hashtags","num_mentions"]]
    numeric_data["user_verified"] = numeric_data["user_verified"].astype(int)
    textual_data = tweet_data[['text', 'user_screen_name']].values
    textual_data = get_text_features(textual_data)
    return numeric_data.values, textual_data


# read dataset
def get_train_data(path):
    original_data = pd.read_excel(path,header=0)
    labels = original_data["is_fake_news"].astype(int)
    numeric_data, textual_data = get_features(original_data[['text', 'user_screen_name',"retweet_count","user_verified","user_friends_count","user_followers_count","user_favourites_count","num_hashtags","num_mentions"]])
    return numeric_data, textual_data, labels


