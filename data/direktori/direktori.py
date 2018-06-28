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

fileyaml = 'direktori.yml'
fileinput = 'input.txt'
filestopword = 'stopword-id.txt'

rel_dir = '/data/direktori/'

if not os.path.isfile(fileyaml):
    fileyaml = os.getcwd()+rel_dir+fileyaml
    fileinput = os.getcwd()+rel_dir+fileinput
    filestopword = os.getcwd()+rel_dir+filestopword
    
with open(fileyaml) as f:
    entdic = yaml.load(f)
    debug = entdic['debug']
    #debug = True

    
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
   
def get_entity(sentence, entname=None):
    """Identifikasi entity pada sebuah input"""
    #wordtoken daftar token menurut input.txt file
    wordtoken = nltk.word_tokenize(cleantag(words))
    wordtoken = list(set(wordtoken))
    wordtoken = stemlist(wordtoken)
    
    #mengecilkan sentence dengan token word input
    if debug: print("daftar token:",wordtoken)
    output = nltk.word_tokenize(sentence)

    for i in wordtoken:
        try:
            output.pop(output.index(i)) 
        except:
            pass


    if debug: print('hasil reduksi:',output)

    #masukkan ke dict entity -> kalau kosong reply dtn dic entity
    if len(output) != 0:
        for i in entdic['entity']:
            if i['value']=='None':
                i['value']=' '.join(output)
                break
            #if debug: print("dapat entity:",i)
    else:
        #if debug: print("belum ada entity\n")
        for i in entdic['entity']:
            #
            if i['value'] == "None":
                output = i
            else:
                output = i

    #loop check akhir
    for i in entdic['entity']:
        if i['value']=='None':
            output = i
            break
        else:
            
            #Entities ready for process
            output = "{'name':'None','followup':'None','prompt':'oke'}"
            

    if debug: print("reply:",output)
    return output

def input(sentence):
    #parse all sentence
    #put variable on the intent
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    #instrukdi di stem terlebih dahulu
    sentence = stemmer.stem(sentence)
    
    #lalu di parse untuk mencari entity
    reply=get_entity(sentence)

    if reply == "{'name':'None','followup':'None','prompt':'oke'}":
        
        process()
        
    if debug: print("langsung dari input:",sentence)
    if debug: print("Reply:",reply)
    
    #kalau entities sudah lengkap. lekas proses
    
    return reply

def process():
    global entdic
    input=entdic['entity'][0]['value']
    print("memprosess direktori:", input)

    if input=="chatbot":
        direktori="E:\\DATA\\Python\\3.6\\Words\\cipichatbot\\"
    elif input == "musik":
        direktori="E:\\Downloads\\Music\\"
    elif input == "ableton":
        direktori="E:\\DATA\\Ableton\\"
    elif input == "gambar":
        direktori="E:\\IRQ\\Pictures\\"
    elif input == "download":
        direktori="E:\\Downloads\\"
    elif input == "torrent":
        direktori="E:\\Downloads\\Torrent\\"
    else:
        direktori="E:\\DATA\\"


    try:
        import subprocess
        subprocess.Popen(r'explorer '+ direktori)

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
    input("buka direktori chatbot")
