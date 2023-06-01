import requests
import re
import pandas as pd
import lxml
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from nltk.corpus import cmudict
from textstat.textstat import textstatistics

tokenizer = RegexpTokenizer(r'\w+')
#stopword listing
stopword_list = []
stopword_file_list = ["StopWords_Auditor.txt","StopWords_Currencies.txt","StopWords_DatesandNumbers.txt","StopWords_Generic.txt",
  "StopWords_GenericLong.txt","StopWords_Geographic.txt","StopWords_Names.txt"]
for file_list in stopword_file_list:
  fs = open("StopWords/"+file_list,"r")
  for line in fs:
    stopword_list.append(re.split("\s",line[:-1],1)[0])

#positive and negative dictionary creation
positive_dict = []
negative_dict = []
fs = open("MasterDictionary/positive-words.txt", "r")
for line in fs:
  if line[:-1] not in stopword_list: 
    positive_dict.append(line[:-1])
fs = open("MasterDictionary/negative-words.txt", "r")
for line in fs:
  if line[:-1] not in stopword_list: 
    negative_dict.append(line[:-1])

InputDataFrame = pd.read_excel("output.xlsx")
urls = InputDataFrame.iloc[:,1].values
i=0
for url in urls:
  print(url)
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
  words_temp = tokenizer.tokenize(raw_text)
  lemmatizer = WordNetLemmatizer()
  words = []
  positive_score = 0
  negative_score = 0
  complex_word_count = 0
  syllable_count = 0
  character_count = 0
  for word in words_temp:
    if word not in stopword_list:
      words.append(word)
      character_count = character_count + len(word)
    if word not in stopword_list and textstatistics().syllable_count(word) >= 2:
      complex_word_count = complex_word_count + 1
      syllable_count = syllable_count + textstatistics().syllable_count(word)
    if word in positive_dict:
      positive_score = positive_score + 1
    if word in negative_dict:
      negative_score = negative_score + 1

  pronoun_count = len(re.findall("(\s+I\s+)|(\s+I\,)|(\s+we\s+)|(\s+we\,)|(\s+my\s+)|(\s+my\,)|(\s+ours\s+)|(\s+ours\,)|(\s+us\s+)|(\s+us\,)", raw_text))
  awl = character_count/len(words)
  scpw = syllable_count/len(words)
  asl = len(words)/len(sentences)
  percent_of_cmplx_word = complex_word_count/len(words)
  fog_index =  0.4 * (asl + percent_of_cmplx_word)
  polarity_score = (positive_score - negative_score)/ ((positive_score + negative_score) + 0.000001)
  subjectivity_score = (positive_score + negative_score)/ (len(words) + 0.000001)
  print(positive_score,negative_score,polarity_score,subjectivity_score,asl,complex_word_count,len(words),scpw,awl,pronoun_count)
  InputDataFrame.iloc[i,2:] = [positive_score,negative_score,polarity_score,subjectivity_score,asl,percent_of_cmplx_word,fog_index,asl,complex_word_count,len(words),scpw,pronoun_count,awl]
  i=i+1
InputDataFrame.to_excel('result.xlsx')

