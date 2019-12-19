import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from socket import error as SocketError
import errno
import requests

link_kids = pd.read_csv("file/url_kids.csv")
url_kids = link_kids["URLKids"].tolist()

count = 1
number = []
link =[]
mykey = []

for pg in url_kids:
    
    ind = url_kids.index(pg)
    no = count
   
    try:
        html = urlopen(pg)
    
    except HTTPError:
        keyword = "No keyword given"
    
    except URLError:
        keyword = "No keyword given"
    
    except SocketError:
        keyword = "No keyword given"

    else:
        html = html.read()
        soup = BeautifulSoup(html)
    
        key = soup.find("meta",  attrs={"name":('keywords', 'KeyWords')})
        
        if key:
            if key.has_attr('content'):
                keyword = key["content"]
            elif key.has_attr('value'):
                keyword = key["value"]
        else:
            keyword = "No keyword given" 
        #keyword = key["content"] if key else "No keyword given" 
    
    number.append(no)
    link.append(pg)
    mykey.append(keyword)
    count = count+1

list_of_tuples = list(zip(number, link, mykey))    

kids_link = pd.DataFrame(list_of_tuples, columns = ['No','Link', 'Keywords'])
export_csv = kids_link.to_csv (r'file/keyword/keywords_kids.csv', index = None, header=True)