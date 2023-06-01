import requests
import lxml
from bs4 import BeautifulSoup
from collections import defaultdict
import math
import nltk
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize


stop
url = "https://insights.blackcoffer.com/coronavirus-impact-on-energy-markets-2/"
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
f = requests.get(url, headers = headers)
soup = BeautifulSoup(f.content, 'lxml')
movies = soup.find('div' ,{
    'class': 'td-post-content'
}).find_all('p')
raw_text =""
for x in movies:
  raw_text += str(x.getText())

sentences = sent_tokenize(raw_text)
lemmatizer = WordNetLemmatizer()
word_counts = defaultdict(lambda: [0,0])

