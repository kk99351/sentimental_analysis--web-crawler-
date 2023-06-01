import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

from collections import defaultdict
import math

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import pandas as pd

df = pd.read_csv('imdb_rev.csv')
lemmatizer = WordNetLemmatizer()
word_counts = defaultdict(lambda: [0,0])

STOP_WORDS = stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')
sentiment = list(df['sentiment'])

done = 0

total_positive_words = 0
total_negative_words = 0

total_positive_reviews = 0
total_negative_reviews = 0

for i, review in enumerate(list(df['review'])):
    if sentiment[i] == 'positive':
        total_positive_reviews += 1
    else:
        total_negative_reviews += 1
    
    for token in tokenizer.tokenize(review):
        token = token.lower()
        token = lemmatizer.lemmatize(token)
        if token not in STOP_WORDS:
            if sentiment[i] == 'positive':
                word_counts[token][1] += 1
                total_positive_words  += 1
            else:
                word_counts[token][0] += 1
                total_negative_reviews += 1
word_counts = sorted(word_counts.items(), key=lambda x: x[1][0] + x[1][1], reverse=True)[:5000]
word_counts = defaultdict(lambda: [0,0], word_counts)

def calculate_word_probability(word, sentiment):
    if sentiment == 'positive':
        return math.log((word_counts[word][1] + 1)/(total_positive_words + 5000))
    else:
        return math.log((word_counts[word][0] + 1)/(total_negative_words + 5000))

def calculate_review_probability(review, sentiment):
    if sentiment == 'positive':
        probability = math.log(total_positive_reviews / len(df))
    else:
        probability = math.log(total_negative_reviews / len(df))

    for token in tokenizer.tokenize(review):
        token = token.lower()
        token = lemmatizer.lemmatize(token)
        if token not in STOP_WORDS:
            probability += calculate_word_probability(token, sentiment)
    return probability

def predict(review):
    if calculate_review_probability(review, 'positive') > calculate_review_probability(review, 'negative'):
        return 'positive'
    else:
        return 'negative'

print(predict('very good'))
print(predict('Not so good... I found it somewhat boring'))