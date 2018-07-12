import soundfile
import sounddevice
import codecs
import glob
import multiprocessing
import re
import nltk
import gensim.models.word2vec as w2v
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import gensim
from sklearn.model_selection import train_test_split
import keras
import logging
import time


#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info('loaded at :'+str(time.asctime()))

debug=True   
debug2=True   #print sektor

smodel = keras.models.load_model("./model/chippy_v1.model")    #keyword detect
model = keras.models.load_model("./model/model2.chatbot")      #command intent detect

import pickle
intent = pickle.load(open("i_intent.p", 'rb'))
i_integer_encoded = pickle.load(open("i_integer_encoded.p", "rb"))
i_onehot_encoded = pickle.load(open("i_onehot_encoded.p", 'rb'))

nltk.download('punkt')

# Second dimension of the feature is dim2
feature_dim_2 = 11

# # Feature dimension
feature_dim_1 = 20
channel = 1
epochs = 50
batch_size = 100
verbose = 1
num_classes = 2

interrupted = False
yesno_state = False
listen_state = False
talk_state = False
cmd = ""
headless = False
i_quit = False

from chat_wordvec import *
from intent_builder import *
from chat_iface import *
import chitchat as chitchat
from preprocess import *

humanstate={
    'sequence': 0,
    'intent':'None',
    'intentscore': 0.,
    'followup': 'None',
    'intentfu': 'None',
    'context': 'None',
    'content': 'None',
    'lastmsg': 'None'
}
botstate={
    'sequence': 0,
    'intent':'None',
    'intentscore': 0.,
    'followup': 'None',
    'intentfu': 'None',
    'context': 'None',
    'content': 'None',
    'lastmsg': 'None',
    'prompt': 'None',
    'process': 'None'
}

escape_dict={'\a':r'\a',
             '\b':r'\b',
             '\c':r'\c',
             '\f':r'\f',
             '\n':r'\n',
             '\r':r'\r',
             '\t':r'\t',
             '\v':r'\v',
             '\'':r'\'',
             '\"':r'\"'}

def raw(text):
    """Returns a raw string representation of text"""
    new_string = ''
    for char in text:
        try: 
            new_string += escape_dict[char]
        except KeyError: 
            new_string += char
    return new_string

def pred_intent(sentence):
    """memprediksi masuk intent apakah sebuah kalimat."""
    
    vectorized_sentence = np.array([swv_ar(twl(sentence))])
    predictions = model.predict(vectorized_sentence)
    cls_pred = np.argmax(predictions,axis=1)

    jawaban = intent[list(i_integer_encoded).index(cls_pred[0])]

    result={'intent' : jawaban, 'score' : predictions.max(), 'sentence' : sentence}
    logging.warning("Pred intent:", result)
    return result


def sequence(sentence, humanstate, botstate):
    """urutan memproses sebuah kalimat menjadi sebuah reply"""
    #do some filtering escape
    sentence = raw(sentence)

    if debug: print("\nSENTENCE:", sentence)
    logging.warning("SENTENCE:")
    logging.warning("A:" + str(sentence))

    humanstate, botstate = input_classifier(sentence, humanstate, botstate)

    logging.info("HUMAN STATE:" + str(humanstate))
    logging.info("BOT STATE:" + str(botstate))
            
    humanstate, botstate = input_processor(humanstate, botstate)

    output, humanstate, botstate = reply_creator(humanstate, botstate)
    return output, humanstate, botstate


def input_classifier(sentence, humanstate, botstate):
    """Fase pertama - tentukan minimum skor dan masukkan intent chitchat apa bila bukan command"""
    #PROSES IDENTIFIKASI SKOR CLASSIFIER
    result = pred_intent(sentence)
    humanstate['lastmsg'] = sentence
    humanstate['intent'] = result['intent']
    humanstate['intentscore'] = result['score']
    scoremasukan = result['score']
    minimum_score = min_pred[result['intent']]
    
    #PERUBAHAN INTENT APABILA SCORE DIBAWAH YANG DI TENTUKAN
    if  scoremasukan > minimum_score :
        pass
    else:
        logging.info("scoremasukan:"+str(scoremasukan))
        #karena lebih kecil dari score- maka ini chitchat
        humanstate['intent'] = 'chitchat'
    return humanstate, botstate

def input_processor(humanstate, botstate):
    """Fase kedua - lihat intent goodbye, cek apakah sebuah followup, apabila benar maka ambil semua field yg di perlukan
    lalu panggil function dan method berkaitan dengan intent."""
    global listening

    botstate['lastmsg'] = botstate['prompt']
    
    if botstate['intent'] == 'goodbye':
        if debug: print("\nGoodbye\n")
        logging.warning("Intent is goodbye")
        listening = False
        
    #EXEKUSI FOLLOWUP SECARA PRIORITAS - apakah bot sebelumnya minta followup?
    if botstate['followup'] != 'None':
            #kalau negasi setelah followup bot maka batal semua
            if humanstate['intent'] == 'negasi':
                botstate['intent'] = 'None'
                botstate['followup'] = 'None'
                botstate['name'] = 'None'
                botstate['prompt'] = 'batal'
                instruction = "{'name' : 'None', 'followup' : 'None', 'intentfu' : 'None', 'prompt' : 'pembatalan'}"
                logging.info("Sector A")
            else:
                instruction = botstate['intentfu'] + '.' + "input(\'" + humanstate['lastmsg'] + "\')"
                logging.info("Sector B")
    else:
        
        if humanstate['intent'] != 'chitchat':
            logging.info("Sector C")
            instruction = humanstate['intent'] + '.' + "input(\'" + humanstate['lastmsg'] + "\')"
        else:
            if humanstate['intent'] == 'goodbye':
                logging.info("Sector D")
                instruction = humanstate['intent'] + '.' + "input(\'" + humanstate['lastmsg'] + "\')"
                logging.info("Quit detected, i will quit")
            #TARUH DISINI UNTUK RUTIN CHITCHAT - dan kurang mengerti apa yang di bilang.
        
        #default EXIT
        logging.info("Sector E")
        instruction = humanstate['intent'] + '.' + "input(\'" + humanstate['lastmsg'] + "\')"

        #print(instruction, "intent driven")
    
    logging.warning("try exec instruction:"+str(instruction))
    
    try:
        #EXECUTE COMMAND =======================
        rslt = eval(instruction)
        # ======================================            
    except Exception as e:
        logging.error("ERROR- Problem doing eval(instruction) in chat_proc.py input_processor: "+str(instruction) + str(e))
    
    #proses kembali jawaban dari EVAL
    #rslt bisa sebuah dict. contoh: "{'name':'None','followup':'None','intentfu':'None','prompt':'pembatalan'}"
    #atau bukan
    if type(rslt) is not dict:
        botstate['intent'] = 'None'
        botstate['followup'] = 'None'
        botstate['prompt'] = 'oke'
        
    else:
        botstate['intent'] = humanstate['intent']
        botstate['followup'] = rslt['name']
        botstate['intentfu'] = rslt['followup']
        botstate['prompt']= rslt['prompt']

    return humanstate, botstate


def reply_creator(humanstate, botstate):
    """Pembentukan jawaban akhir dari sebuah reply - disini dirubah dari kondisi humanstate dan botstate
    lalu proses apa yang perlu di proses"""
    output = botstate['prompt']
    
    if botstate['process'] != 'None':
        print("Mencoba memproses :", botstate['process'])
        eval(botstate['process'])

    
    logging.info("\nEND STATE")
    logging.info("human state:"+str(humanstate))
    logging.info("bot state:"+str(botstate))
    logging.info("\n")
            
    logging.warning("B:" + "\n" + str(humanstate) + "\n" + str(botstate) + "\n\n")
    return output, humanstate, botstate    
