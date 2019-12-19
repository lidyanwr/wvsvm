import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

all_data = pd.read_csv("file/clean_data.csv")
clean_data = all_data.dropna()

corpus_all = clean_data["Data"].to_numpy()

def get_top_n_words(corpus):
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq

alldata = get_top_n_words(corpus_all)
allwords = []
freqData = []
for word, freq in alldata:
    allwords.append(word)
    freqData.append(freq)

list_of_keyword = list(zip(allwords, freqData))    
countWord = pd.DataFrame(list_of_keyword, columns = ['Term','TotalFrequency'])
countWord = countWord.sort_values(by='TotalFrequency', ascending=False)
export_csv = countWord.to_csv (r'file/keyword/countAllWord.csv', index = None, header=True)

newDFKeyword = countWord

dictkeyword = [line.rstrip('\n') for line in open('file/keyword/unique_keyword.txt')]
def deleteWord(key):
    if key not in dictkeyword:
        indexTerm = newDFKeyword[newDFKeyword['Term'] == key].index
        newDFKeyword.drop(indexTerm , inplace=True)
    return (newDFKeyword)

newDFKeyword["Term"].apply(deleteWord)

export_csv = newDFKeyword.to_csv (r'file/keyword/KeywordInAllDoc.csv', index = None, header=True)    