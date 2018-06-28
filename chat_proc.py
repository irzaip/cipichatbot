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

smodel = keras.models.load_model("./model/chippy_v1.model")    #keyword detect
model = keras.models.load_model("./model/model2.chatbot")      #command intent detect

import pickle
intent = pickle.load(open("i_intent.p",'rb'))
i_integer_encoded = pickle.load(open("i_integer_encoded.p","rb"))
i_onehot_encoded = pickle.load(open("i_onehot_encoded.p",'rb'))


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


def pred_intent(sentence):
    """memprediksi masuk intent apakah sebuah kalimat."""
    predictions=model.predict(np.array([swv_ar(twl(sentence))]))
    cls_pred = np.argmax(predictions,axis=1)

    jawaban = intent[list(i_integer_encoded).index(cls_pred[0])]

    result={'intent': jawaban, 'score': predictions.max(), 'sentence': sentence}
    return result


def sequence(sentence,humanstate,botstate):
    """urutan memproses sebuah kalimat menjadi sebuah reply"""
    if debug: print("\nSENTENCE:",sentence)
    logging.info("SENTENCE:")
    logging.info("A:"+str(sentence))
    humanstate,botstate = input_classifier(sentence,humanstate,botstate)
    humanstate,botstate = input_processor(humanstate,botstate)

    if debug: 
        print("\nBEGIN")
        print("HUMANSTATE:",humanstate)
        print("BOTSTATE:",botstate)

    output,humanstate,botstate = reply_creator(humanstate,botstate)
    return output,humanstate,botstate


def input_classifier(sentence,humanstate,botstate):
    result = pred_intent(sentence)
    humanstate['lastmsg']=sentence
    humanstate['intent']=result['intent']
    humanstate['intentscore']=result['score']
    scoremasukan = result['score']
    minimum_score = min_pred[result['intent']]
    
    #PERUBAHAN INTENT APABILA SCORE DIBAWAH YANG DI TENTUKAN
    if  scoremasukan > minimum_score :
        pass
    else:
        #karena lebih kecil dari score- maka ini chitchat
        humanstate['intent']='chitchat'
    return humanstate,botstate

def input_processor(humanstate,botstate):
    global listening
    botstate['lastmsg']=botstate['prompt']
    
    if botstate['intent']=='goodbye':
        if debug: print("\nGoodbye\n")
        listening=False
        
    #EXEKUSI FOLLOWUP SECARA PRIORITAS - apakah bot sebelumnya minta followup?
    if botstate['followup'] != 'None':
            #kalau negasi setelah followup bot maka batal semua
            if humanstate['intent'] == 'negasi':
                botstate['intent']='None'
                botstate['followup']='None'
                botstate['name']='None'
                botstate['prompt']='batal'
                instruction="{'name':'None','followup':'None','intentfu':'None','prompt':'pembatalan'}"
            else:
                instruction = botstate['intentfu']+'.'+"input(\'"+humanstate['lastmsg']+"\')"
    else:
        
        if humanstate['intent'] != 'chitchat':
            instruction = humanstate['intent']+'.'+"input(\'"+humanstate['lastmsg']+"\')"
        else:
            if humanstate['intent'] == 'goodbye':
                instruction = humanstate['intent']+'.'+"input(\'"+humanstate['lastmsg']+"\')"
                if debug: print("I will quit")
            #TARUH DISINI UNTUK RUTIN CHITCHAT - dan kurang mengerti apa yang di bilang.
        
        #default EXIT
        instruction = humanstate['intent']+'.'+"input(\'"+humanstate['lastmsg']+"\')"

        #print(instruction, "intent driven")
    
    if debug: print(instruction)
    #EXECUTE COMMAND =======================
    rslt = eval(instruction)
    # ======================================            
    
    
    #proses kembali jawaban dari EVAL
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

def reply_creator(humanstate,botstate):
    output=botstate['prompt']
    
    if botstate['process'] != 'None':
        eval(botstate['process'])
    if debug:
        print("\nEND STATE")
        print("HUMAN STATE:",humanstate)
        print("END BOTSTATE:",botstate)
        print("\nREPLY:",botstate['prompt'])
    logging.info("B:"+"\n"+str(humanstate)+"\n"+str(botstate)+"\n\n")
    return output, humanstate, botstate    




def testalk(sentence,s_iface):
    talking = True
    talk(sentence, s_iface)
    while talking:
        if not cek_talk_or_speak(s_iface):
            talking=False
            print("X")
            clear(s_iface)
        else:
            print("_",end='')
            time.sleep(0.02)