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
import logging
import sys

logging.basicConfig(level=logging.ERROR)


lst_alat = ['kipas',
        'kipas angin',
        'lampu',
        'pemasak']

lst_ruangan = ['ruang tamu',
           'ruang kaca',
           'ruang televisi',
           'ruang TV',
           'ruang tengah'
           'ruangan tamu',
           'ruangan kaca',
           'ruangan televisi',
           'ruangan TV',
           'ruangan tengah',
           'ruang makan',
           'dapur',
           'kamar inang'
           ]

lst_instruksi = ['matikan','matiin','mati',
             'nyalakan','nyalain','nyala']


def find_pat(sentence, lists):
    for slist in lists:
        print('finding',slist)
        indx = sentence.find(slist)
        if indx >= 0: 
            print(f"found at index: {indx}")
            return slist
    return False

fileyaml = 'homeauto.yml'
fileinput = 'input.txt'
filestopword = 'stopword-id.txt'

rel_dir = '/data/homeauto/'

if not os.path.isfile(fileyaml):
    fileyaml = os.path.join(os.getcwd(), rel_dir, fileyaml)
    fileinput = os.path.join(os.getcwd(), rel_dir, fileinput)
    filestopword = os.path.join(os.getcwd(), rel_dir, filestopword)
    
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
    global instr
    """Identifikasi entity pada sebuah input"""
    instr = find_pat(sentence, lst_instruksi)
    util = find_pat(sentence, lst_alat)
    room = find_pat(sentence, lst_ruangan)

    if util: entdic['entity'][0]['value'] = util
    if room: entdic['entity'][1]['value'] = room

    if instr and util and room: print(f"Melakukan {instr} {util} untuk {room}")    

    #loop check akhir
    for i in entdic['entity']:
        if i['value']=='None':
            output = i
            break
        else:
            #Entities ready for process
            output = "{'name':'None','followup':'None','prompt':'oke'}"
            

    if debug: print("Reply:",output)
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
        
    logging.info("langsung dari input:"+ str(sentence))
    logging.info("Reply:" + str(reply))
    print("Reply:",reply)
    
    #kalau entities sudah lengkap. lekas proses
    
    return reply

def process():
    global entdic
    util=entdic['entity'][0]['value']
    ruang=entdic['entity'][1]['value']
    print("memprosess homeauto:", instr, util, ruang)

    try:
        import webbrowser
        #url = 'https://www.google.com/search?tbm=isch&tbo=u&source=univ&sa=X&q='+str(gambar)
        #webbrowser.open(url)
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
    input("Matikan kipas ruang tamu")
