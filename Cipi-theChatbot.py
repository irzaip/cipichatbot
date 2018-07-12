
# coding: utf-8

# In[1]:


import sys
import logging
logging.basicConfig(format='%(message)s', level=logging.DEBUG, stream=sys.stdout)

from listens import *
import keras
from preprocess import *
from chat_iface import *
from chat_proc import *


# In[2]:

speech = ""

def process():
    ear.stop()
    pass
    print("Ini prosesnya")


# In[3]:


def transcrib():
    global speech
    speech = transcribe_speech(s_iface)
    if speech == None:
        speech = ""
    print("Ini Transkrip:",speech)


# In[4]:


ear = Listen()
ear.set_process(process)
#ear.start(thres=800, process=process)


# In[5]:


model = keras.models.load_model("./model/chippy_v1.model")


# In[6]:


from selenium import webdriver

headless = False
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
if headless:
    chrome_options.add_argument("--headless")  
    
def start_iface():
    s_iface = webdriver.Chrome(chrome_options=chrome_options)
    s_iface.get('https://translate.google.com/?#id/id')
    assert "Google Translate" in s_iface.title
    talk("saya siap",s_iface)
    return s_iface
    
def mainbrowser(url):
    global m_iface
    m_iface = webdriver.Chrome(chrome_options=chrome_options)
    m_iface.get('https://translate.google.com/?#id/id')


# In[7]:


def relisten_hotword():
    global att_counter, cipi_recognized, attention, speech
    att_counter = 0
    cipi_recognized = False
    attention = False
    speech=""
    time.sleep(1)


# In[8]:


def is_not_a_followup():
    if botstate['followup']=="None":
        return True
    return False    


# In[9]:


s_iface = start_iface()


# In[10]:


debug=True
cipi_recognized=False
ear.debug = False
feature_dim_1 = 20
feature_dim_2 = 11
channel = 1
awake = True

while not cipi_recognized:
    print("Start waiting for hotword...")
    ear.start(thres=1200, timeout=0)
    #ear.write_to_file('test.wav')
    dataaudio=np.array(ear.audiodata).flatten()
    sample = au2mfcc(dataaudio)
    sample_reshaped = sample.reshape(1, feature_dim_1, feature_dim_2, channel)
    y_pred = model.predict(sample_reshaped)
    y_max = np.max(y_pred) #nilai akurasi prediksi
    ypred = np.argmax(y_pred) #yg di prediksi adalah cipi
    cipi_recognized = (y_max>0.9 and ypred==1)
    if cipi_recognized: 
        
        #RANDOMIZE this
        playdetected()
        
        print("Recognized - Predicted:" ,get_labels()[0][ypred],y_max, ypred)

        attention=True
        att_counter = 0
        while attention:
            print("Attention is:",attention)
            rec_speech(s_iface)
            ear.debug = False
            ear.start(thres=800, timeout=5, process=transcrib)
            if speech: #ada kalimat yg disebut dalam bentuk string
                #RANDOMIZE THIS
                playdetected()
                reply,humanstate,botstate = sequence(speech,humanstate,botstate)
                if awake:
                    talk_until_complete(reply,s_iface)
                #if the reply not a followup
                if botstate['followup']=="None": 
                    print("not a followup")
                    relisten_hotword()
            else:
                print("blank speech detected")
                speech = " " #kasih sedikit spasi hack
                att_counter += 1
                if att_counter > 1:
                    relisten_hotword()
                    print("\n=============\nGo to wait mode")

