import numpy as np
import pandas as pd
import nltk
import os, sys, re, collections, string
from operator import itemgetter as at
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import text


# read dataset
def get_data(path):
    original_data = pd.read_excel(path,header=0)
    labels = original_data["is_fake_news"].astype(int)
    # sub_labels = original_data["fake_news_category"]
    numeric_data = original_data[["retweet_count","user_verified","user_friends_count","user_followers_count","user_favourites_count","num_hashtags","num_mentions"]]
    numeric_data["user_verified"] = numeric_data["user_verified"].astype(int)
    textual_data = original_data[['text', 'user_screen_name']].values
    return numeric_data,textual_data,labels


numeric_data,textual_data,labels = get_data("ADAFake/data/electionday_tweets_clean.xlsx")


# in process
# Remove punctuation and unknown characters, convert all text to lower case
path = "ADAFake/data/electionday_tweets_clean.xlsx"
original_data = pd.read_excel(path, header=0)
text_col = original_data[["text"]].applymap(str.lower).replace(re.compile(r"[^\s\w<>_]"), "")
bag_of_words = text_col.applymap(str.split).applymap(collections.Counter)
total_word_count = sum(bag_of_words.values, collections.Counter())
cv = text.CountVectorizer(min_df=1e-06, max_df=0.05)
cv.fit(text_col['text'])
text_0 = cv.transform([text_col.loc[0, 'text']])
{k:v for k,v in zip(cv.get_feature_names(), text_0.toarray()[0]) if v>0}





#tfidf
transformer = TfidfTransformer(smooth_idf=False)
count_vectorizer = CountVectorizer(ngram_range=(1, 2))
counts = count_vectorizer.fit_transform(original_data['text'].values)
tfidf = transformer.fit_transform(counts)


##################
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter
from nltk.tokenize import MWETokenizer

tknzr = TweetTokenizer()
tkn_txt = tknzr.tokenize(txt[:, 0][0])


def get_ngrams(text, n):
    n_grams = ngrams(tknzr.tokenize(text), n)
    return [' '.join(grams) for grams in n_grams]


def mwet_tkn(text):


def get_bag_of_words(text):
    return Counter(text)

get_bag_of_words(get_ngrams(txt[:, 0][0],2))



#######

train=pd.read_csv('ADAFake/data/train.csv')
test=pd.read_csv('ADAFake/data/test.csv')
test.info()
test['label']='t'
train.info()
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer

#data prep
test=test.fillna(' ')
train=train.fillna(' ')
test['total']=test['title']+' '+test['author']+test['text']
train['total']=train['title']+' '+train['author']+train['text']

transformer = TfidfTransformer(smooth_idf=False)
count_vectorizer = CountVectorizer(ngram_range=(1, 2))
counts = count_vectorizer.fit_transform(train['total'].values)
tfidf = transformer.fit_transform(counts)