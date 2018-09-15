import numpy as np
import pandas as pd
import nltk
import os, sys, re, collections, string
from operator import itemgetter as at
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm
from ipywidgets import interact

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

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer

# Remove punctuation and unknown charactars
not_allowed = re.compile(r"[^\s\w<>_]")
sample_doc = not_allowed.sub("", sample_doc)


def clean_text(text):
    return not_allowed.sub("", digits.sub("<NUM>",text.lower()))


def bag_of_words(text):
    return collections.Counter(text.split())

nltk.download('punkt')
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

sample_corpus = " ".join([content for i, (file, content) in enumerate(data.getIterator()) if i<1000])
tokenized_corpus = nltk.word_tokenize(sample_corpus)
# change this to read in your data
finder = nltk.collocations.BigramCollocationFinder.from_words(tokenized_corpus)
finder.apply_freq_filter(4)
# return the 10 n-grams with the highest PMI
finder.nbest(bigram_measures.student_t, 100)

from gensim.models import Phrases
X_words = [content.split() for file, content in itertools.islice(data.getIterator(), 1000)]
bigram = Phrases(X_words, min_count=10, threshold=2)
bigram[X_words[0]]


#tfidf
transformer = TfidfTransformer(smooth_idf=False)
count_vectorizer = CountVectorizer(ngram_range=(1, 2))
counts = count_vectorizer.fit_transform(original_data['text'].values)
tfidf = transformer.fit_transform(counts)