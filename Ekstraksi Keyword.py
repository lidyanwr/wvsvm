import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()

keyword_kids = pd.read_csv("file/keyword/keywords_kids.csv")
keyword_kids["Keywords"] = keyword_kids["Keywords"].replace(np.nan, "No keyword given")

allkeywordskids = []
keywordsprepross = []
unique_keyword = [] 
frequency = {}
myword = []
freqword = []

def getkeyword(raw_text):
    if raw_text != "No keyword given":
        text_1 = BeautifulSoup(raw_text).get_text()
        text_2 = text_1.replace(';', ',')
        words = text_2.lower().split(',')
        kidskeywords = [x for x in words]
        
        for w in kidskeywords:
            word = w.replace("\n", "")
            word = word.replace("\r", "")
            word = word.replace("\t", "")
            allkeywordskids.append(word)
    return(allkeywordskids)

def count_keyword(raw_text):
    text_1 = BeautifulSoup(raw_text).get_text()
    text_2 = text_1.replace(';', ',')
    if raw_text != "No keyword given":
        words = text_2.lower().split(',')
        numbKey = len(words)
    else:
        numbKey = 0
    return(numbKey)

def remove_whitespace(text): 
    return  " ".join(text.split()) 

def prepros_keyword(raw_text):
    letters_only = re.sub("[^a-zA-Z]", " ",str(raw_text))
    spacetext = remove_whitespace(letters_only)
    words = spacetext.split()
    
    lem_words=[]
    for word in words:
        lem_text = lemmatizer.lemmatize(word)
        lem_text = lemmatizer.lemmatize(lem_text, pos ='v')
        lem_words.append(lem_text)

    stop_words = [line.rstrip('\n') for line in open('file/stopwords_en.txt')] #stopwords dari txt
    filtered_text = [word for word in lem_words if word not in stop_words]
    
    for w in filtered_text:
        if len(w)>2:
            keywordsprepross.append(w)
    return (keywordsprepross)

def uniq_keyword(mylist):
    for x in mylist: 
         if x not in unique_keyword: 
            unique_keyword.append(x) 
    return(unique_keyword)

def freq_keyword(mylist):
    for word in mylist:
        count = frequency.get(word,0)
        frequency[word] = count + 1
    frequency_list = frequency.keys()
     
    for words in frequency_list:
        myword.append(words)
        freqword.append(frequency[words])
    return 0

keyword_kids["Keywords"].apply(getkeyword)
keyword_kids["CountKeyword"] = keyword_kids["Keywords"].apply(count_keyword)
prepros_keyword(allkeywordskids)
uniq_keyword(keywordsprepross)
freq_keyword(keywordsprepross)
list_of_keyword = list(zip(myword, freqword))    
freqKeyword = pd.DataFrame(list_of_keyword, columns = ['Term','Frequency'])
freqKeyword = freqKeyword.sort_values(by='Frequency', ascending=False)

with open('file/keyword/keywordKids.txt', 'w', encoding="utf-8") as filehandle:
    for listitem in allkeywordskids:
        filehandle.write('%s\n' % listitem)
        
with open('file/keyword/keywordprepross.txt', 'w', encoding="utf-8") as filehandle:
    for listitem in keywordsprepross:
        filehandle.write('%s\n' % listitem)

with open('file/keyword/unique_keyword.txt', 'w', encoding="utf-8") as filehandle:
    for listitem in unique_keyword:
        filehandle.write('%s\n' % listitem)
        
export_csv = freqKeyword.to_csv (r'file/keyword/KeywordFrequency.csv', index = None, header=True)

