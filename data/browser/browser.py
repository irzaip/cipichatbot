# conversation-flow : v.0.01
# template by Irza Pulungan
# todo:
# memparsing hasil response lalu di cocokkan dengan type

import os
import time
#from ..module import rontok
import yaml
import os
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
from selenium import webdriver

fileyaml = 'browser.yml'
fileinput = 'input.txt'
filestopword = 'stopword-id.txt'

rel_dir = '/data/browser/'

if not os.path.isfile(fileyaml):
    fileyaml = os.getcwd()+rel_dir+fileyaml
    fileinput = os.getcwd()+rel_dir+fileinput
    filestopword = os.getcwd()+rel_dir+filestopword
    
with open(fileyaml) as f:
    entdic = yaml.load(f)
    debug = entdic['debug']
    debug = True

    
with open(fileinput) as f:
    words = f.read()

with open(filestopword) as f:
    stopwords = f.readlines()

def stemlist(lists):
    """Membuat stemasi pada sebuah list"""
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    for i in range(len(lists)):
        lists[i]=stemmer.stem(lists[i])
    return lists

def cleantag(raw_html):
    """Membersihkan input dari tag html"""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
   

def input(sentence):
    #parse all sentence
    #put variable on the intent
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    #instrukdi di stem terlebih dahulu
    sentence = stemmer.stem(sentence)
    
    #lalu di parse untuk mencari entity

    print("THE SENTENCE IS:", sentence)
    if sentence!="keluar":
        process(sentence)
        reply={'name': 'informasi', 'followup': 'browser', 'method': 'ask', 'type': 'string', 'required': True, 'value': 'None', 'prompt': 'ya'}
    else:
        reply={'name':'None','followup':'None','prompt':'Keluar'}        
        
    if debug: print("langsung dari input:",sentence)
    if debug: print("Reply:",reply)
    
    #kalau entities sudah lengkap. lekas proses
    
    return reply

def process(sentence):
    global entdic
    print("Sektor P- process")
    command=sentence
    print("memprosess Browser:", command)

    try:
        import webbrowser
        url = 'https://www.google.com/search?source=hp&q='+str(command)
        webbrowser.open(url)
    except:
        pass
    
 #   chrome_options = webdriver.ChromeOptions()
 #   chrome_options.add_argument("--use-fake-ui-for-media-stream")
 #   m_iface = webdriver.Chrome(chrome_options=chrome_options)
 #   m_iface.get('https://www.google.com/search?tbm=isch&tbo=u&source=univ&sa=X&q='+str(gambar))
    time.sleep(0.1)
    #RESET BY LOADING AGAIN THE YAML FILE
    with open(fileyaml) as f:
        entdic = yaml.load(f)
        debug = entdic['debug']


if __name__ == '__main__':
    input("Saya mau lihat gambar kuda terbang")
