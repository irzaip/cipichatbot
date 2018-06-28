
# coding: utf-8

# In[3]:


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
import pprint


# In[4]:


import keras
smodel = keras.models.load_model("./model/chippy_v1.model")
model = keras.models.load_model("/model/model1.chatbot")


# In[5]:


# Second dimension of the feature is dim2
feature_dim_2 = 11

# # Feature dimension
feature_dim_1 = 20
channel = 1
epochs = 50
batch_size = 100
verbose = 1
num_classes = 2


# In[6]:


interrupted = False
yesno_state = False
listen_state = False
talk_state = False
cmd = ""
headless = False
i_quit = False


# ### WORD TOKEN UTILITY

# In[7]:


from chat_wordvec import *
from intent_builder import *
from chat_iface import *
import chitchat as chitchat
from preprocess import *


# In[8]:


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


# In[9]:


def pred(sentence):
    predictions=model.predict(np.array([swv_ar(twl(sentence))]))
    cls_pred = np.argmax(predictions,axis=1)
   
    result={'intent': intent[cls_pred[0]], 'score': predictions.max(), 'sentence': sentence}
    return result


def sequence(sentence,humanstate,botstate):
    print("SENTENCE:",sentence)
    humanstate,botstate = input_classifier(sentence,humanstate,botstate)
    humanstate,botstate = input_processor(humanstate,botstate)
    print("HEREBOT:",botstate)
    output,humanstate,botstate = reply_creator(humanstate,botstate)
    return output,humanstate,botstate


# In[26]:


listening = False

def input_classifier(sentence,humanstate,botstate):
    result = pred(sentence)
    humanstate['lastmsg']=sentence
    humanstate['intent']=result['intent']
    humanstate['intentscore']=result['score']
    
    #PERUBAHAN INTENT APABILA SCORE DIBAWAH YANG DI TENTUKAN
    if result['score'] > min_pred[result['intent']]:
        pass
    else:
        #print('i change to noting')
        humanstate['intent']='chitchat'
    return humanstate,botstate

def input_processor(humanstate,botstate):
    global listening
    botstate['lastmsg']=botstate['prompt']
    
    if botstate['intent']=='goodbye':
        print("Goodbye")
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
                print(instruction)
    else:
        
        if humanstate['intent'] != 'chitchat':
            instruction = humanstate['intent']+'.'+"input(\'"+humanstate['lastmsg']+"\')"
            print(instruction)
        else:
            if humanstate['intent'] == 'goodbye':
                print("I will quit")
            
            listening = False
            instruction='print("I QUIT")'
            try:
                s_iface.close()
            except:
                pass
            #TARUH DISINI UNTUK RUTIN CHITCHAT - dan kurang mengerti apa yang di bilang.
        print(instruction, "intent driven")
        
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
    pprint.pformat(humanstate)
    print(pprint.pformat(botstate))
    return output, humanstate, botstate    


# min_pred = {'lihat_gambar': 0.2 ,
#             'cctv_lewatmana': 0.2, 
#             'salam': 0.1, 
#             'affirmasi': 0.1,
#             'negasi': 0.1,
#             'goodbye': 0.1}

# In[11]:


sequence("see you",humanstate,botstate)


# In[12]:


import soundfile
import itertools
import time
import librosa
import sounddevice


DURATION=20
gain=10
high=2000
low=100
screenwidth=79
predicting=False


def record(length=1, reclength=1, filename=None, thres=0):
    """ 
    Merekam suara secara stream dan metode callback
    """

    global cumulated_status, end_count, start_count, recording, magnitudo, audiodata, predicting, i_quit, listening
    predicting=False
    listening=True
    end_count=False
    start_count = 0
    recording=False
    magnitudo=[]
    audiodata=[]
    try:
        import sounddevice as sd

        #samplerate = sd.query_devices(args.device, 'input')['default_samplerate']
        samplerate = 16000.0

        delta_f = (high - low) / screenwidth
        fftsize = np.ceil(samplerate / delta_f).astype(int)
        low_bin = int(np.floor(low / delta_f))

        cumulated_status = sd.CallbackFlags()

        def callback(indata, frames, time, status):
            global cumulated_status, audiodata, magnitudo, end_count, start_count, recording, smodel, predicting, i_quit
            
            cumulated_status |= status
            if any(indata):
                magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
                magnitude *= gain / fftsize

                rms = librosa.feature.rmse(S=indata)
                rms = int(rms*32768)
                start_count += 1
                if rms>=thres:
                    if not recording :                    #and not end_count
                        #print("Start record")
                        recording = True
                        start_count = 0
                        
                        
                if recording:
                    audiodata.extend(itertools.chain(indata.tolist()))
                    magnitudo.append(magnitude)
                    if start_count == int(samplerate / (samplerate * DURATION / 1000)):
                        #print("End record")
                        start_count=0
                        end_count=True
                        recording=False
                        try:
                            if not predicting:
                                print("Predict")
                                soundfile.write("temp.wav",audiodata,16000)
                                predict("temp.wav", model=smodel)
                                predicting=False
                            pass
                        except:
                            pass
                        audiodata=[]



        with sd.InputStream(device=None, channels=1, callback=callback,
                            blocksize=int(samplerate * DURATION / 1000),
                            samplerate=samplerate):
            while True:
                #response = input()
                #if response in ('', 'q', 'Q'):
                if listening==False:
                #time.sleep(length)
                    break
            if filename!=None: soundfile.write(filename,audiodata,16000)

        if cumulated_status:
            logging.warning(str(cumulated_status))
    except Exception as e:
        print(e)


# In[13]:



# Predicts one sample
def predict(filepath, model):
    
    global s_iface, humanstate, botstate,predicting
    predicting=True
    sv,sr = soundfile.read('./Ring09.wav')
    sample = wav2mfcc(filepath)
    sample_reshaped = sample.reshape(1, feature_dim_1, feature_dim_2, channel)
    y_pred = model.predict(sample_reshaped)
    y_max = np.max(y_pred)
    ypred = np.argmax(y_pred)
    if y_max>0.9 and ypred==1:
        followup = False
        print("Predicted:" ,get_labels()[0][ypred],y_max, ypred)
        sounddevice.play(sv,samplerate=16000)
        #sudah di kenali 
        
        speech = get_speech(s_iface)
        
        reply,humanstate,botstate = sequence(speech,humanstate,botstate)
        clear(s_iface)
        testalk(botstate['prompt'],s_iface)
        print(botstate['followup'])
        
        if botstate['followup'] != 'None':
            followup=True
            print('followup teridentifikasi')
        
        while followup:
            playya()
            speech = get_speech(s_iface)
            reply,humanstate,botstate = sequence(speech,humanstate,botstate)
            print('sudah diambil')
            clear(s_iface)
            testalk(botstate['prompt'],s_iface)
            if botstate['followup'] != 'None':
                followup=True
                
            else:
                followup=False
                break
    predicting=False
    return get_labels()[0][ypred]


# In[17]:


from selenium import webdriver


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
if headless:
    chrome_options.add_argument("--headless")  
    
def start_iface():
    global s_iface
    s_iface = webdriver.Chrome(chrome_options=chrome_options)
    s_iface.get('https://translate.google.com/?#id/id')
    assert "Google Translate" in s_iface.title

    
def mainbrowser(url):
    global m_iface
    m_iface = webdriver.Chrome(chrome_options=chrome_options)
    m_iface.get('https://translate.google.com/?#id/id')


# In[18]:


from chat_iface import *


# In[16]:


start_iface()


# try:
#     talk("mau nonton willy wonka?", s_iface)
# except Exception as e:
#     del s_iface
#     start_iface()
#     talk("Tolong di ulang lagi", s_iface)

# In[19]:


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


# In[21]:


predict("temp.wav",model=smodel)


# In[22]:


record(length=55,filename="record.wav",thres=1100)
print("END PREDICTING+++++++++++++++")

