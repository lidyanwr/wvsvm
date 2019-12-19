import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from socket import error as SocketError
from http.client import IncompleteRead
import numpy as np

kidsurl = pd.read_csv("file/url_kids.csv")
arrayKids = kidsurl.iloc[:, 0].tolist()

link =[]
data = []
category = []
count = 1
mykey = []

for pg in arrayKids:
    try:
        html = urlopen(pg)
    
    except HTTPError:
        text = np.nan
        keyword = np.nan
    except URLError:
        text = np.nan
        keyword = np.nan
    except SocketError:
        text = np.nan
        keyword = np.nan
    except IncompleteRead:
        text = np.nan
        keyword = np.nan
    else:
        html = urlopen(pg).read()
        soup = BeautifulSoup(html)
        key = soup.find("meta",  attrs={"name":('keywords', 'KeyWords')})
        
        if key:
            if key.has_attr('content'):
                keyword = key["content"]
            elif key.has_attr('value'):
                keyword = key["value"]
        else:
            keyword = np.nan
        #keyword = key["content"] if key else "No keyword given" 
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = ' '.join(chunk for chunk in chunks if chunk)
    
    print(count, pg)
    count = count+1
    
    link.append(pg)
    data.append(text)
    mykey.append(keyword)
    category.append("Kids")
    

list_kids = list(zip(link, data, category))    
DFKids = pd.DataFrame(list_kids, columns = ['Link','Data', 'Category'])

export_csv = DFKids.to_csv (r'file/kids_data.csv', index = None, header=True)


