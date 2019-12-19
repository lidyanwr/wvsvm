import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk 
import string 
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 


df_gen = pd.read_csv("file/general_data.csv")
df_kids = pd.read_csv("file/kids_data.csv")
df_all = pd.concat([df_gen, df_kids])

alldata = df_all.dropna()

def remove_whitespace(text): 
    return  " ".join(text.split()) 

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

# text cleansing function
def prepros_word(raw_text):
    
    lemmatizer=WordNetLemmatizer()
    #1. Remove non-letters with regex
    text_1 = BeautifulSoup(raw_text).get_text()
    text_1 = text_1.replace("’", "'")
    text2 = decontracted(text_1)
    lowertext = text2.lower()
    letters_only = re.sub("[^a-zA-Z]", " ",str(lowertext))
    
    # 2. Remove whitespace
    spacetext = remove_whitespace(letters_only)
    
    # 3. Convert to lower case
    words = spacetext.split()
    # 4. Lemmatisasi
    lem_words=[]
    for word in words:
        lem_text = lemmatizer.lemmatize(word)
        lem_text = lemmatizer.lemmatize(lem_text, pos ='v')
        lem_words.append(lem_text)
    # 4. Remove stop words
    #stop_words = set(stopwords.words("english")) --> stopwords dari nltk
    stop_words = [line.rstrip('\n') for line in open('file/stopwords_en.txt')] #stopwords dari txt
    filtered_text = [word for word in lem_words if word not in stop_words]
    # 5. Join the words back into one string separated by space & return, remove the short text
    return(" ".join(w for w in filtered_text if len(w)>2 and len(w)<25))

clean_data = alldata
clean_data['Data'] = clean_data['Data'].apply(prepros_word)
clean_data.loc[clean_data['Category'] == "Kids", 'CategoryIndex'] = 1
clean_data.loc[clean_data['Category'] == "General", 'CategoryIndex'] = -1
clean_data['Category'] = clean_data.Category.astype('category')
clean_data['CategoryIndex'] = clean_data.CategoryIndex.astype('category')
clean_data = clean_data.dropna()

export_csv = clean_data.to_csv (r'file/clean_data.csv', index = None, header=True)