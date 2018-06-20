
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as bs
import nltk
import secrets
import re
import itertools


# In[2]:


topic='cemen'


# In[3]:


def build_structure(string):
    return [' '.join(window) for n in range(len(string)) for
            window in windows(string.split(), n + 1, n)]

def windows(iterable, length=2, overlap=0):
    it = iter(iterable)
    results = list(itertools.islice(it, length))
    while len(results) == length:
        yield results
        results = results[length-overlap:]
        results.extend(itertools.islice(it, length-overlap))

def clean_word(string):
    pattern = re.compile('[\W_]+')
    words = []
    for word in string.split():
        word = re.sub(pattern, ' ', word)
        words.append(word)
    return ' '.join(words)

def make_keywords(string):
    string = clean_word(string.lower())
    keywords = []
    for phrase in build_structure(string):
        if len(list(phrase.split())) >= 1 and len(list(phrase.split())) <= 2:
            if phrase is not None and phrase.strip() != '':
                keywords.append(phrase)
    return secrets.choice(keywords)

def kaskus_search(topic, maxword=25):
    
    topic = make_keywords(topic)
    search_url = 'https://www.kaskus.co.id/search?q='

    page = requests.get(search_url+topic)

    sp = bs(page.text,"html.parser")

    #GET THE THREADS LINKS FROM MAIN PAGE
    thrds = []
    for a in sp.findAll("a",href=True):
        if a['href'].find('/thread/') != -1:
            thrds.append(a['href'])

    rsl = []
    for thrd in thrds:
        page = requests.get(thrd)
        sp = bs(page.text,"html.parser")

    #ambil konten di class entry - tapi dari mulai index 2
        rs = sp.findAll('div',{'class': 'entry'})
        for i in range(2,len(rs)):
            tx = rs[i].getText()
            if len(nltk.word_tokenize(tx)) < maxword:
                rsl.append(tx)
                
    result=secrets.choice(rsl)
    return result


# In[30]:


if __name__ == '__main__':
    print(kaskus_search("cemen"))

