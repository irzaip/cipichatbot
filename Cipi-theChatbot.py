# coding: utf-8
import logging
from listens import *
import keras
from preprocess import *
from chat_iface import *
from chat_proc import *
from selenium import webdriver



logging.basicConfig(filename='cipi.log', format='%(message)s', level=logging.INFO)


def process():
    ear.stop()
    pass
    print("Ini prosesnya")


# In[3]:


def transcrib():
    global speech
    speech = transcribe_speech(s_iface)
    if speech is None:
        speech = ""
    print("Ini Transkrip:", speech)


# In[4]:


ear = Listen()
ear.set_process(process)
#ear.start(thres=800, process=process)


# In[5]:


model = keras.models.load_model("./model/chippy_v1.model")


# In[6]:


headless = False
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
if headless:
    chrome_options.add_argument("--headless")  


def start_iface():
    s_iface = webdriver.Chrome(chrome_options=chrome_options)
    s_iface.set_window_position(-10000, 0)

    s_iface.get('https://translate.google.com/?#id/id')
    assert "Google Translate" in s_iface.title
    talk("saya siap", s_iface)
    return s_iface
    

def mainbrowser(url):
    global m_iface
    m_iface = webdriver.Chrome(chrome_options=chrome_options)
    m_iface.get('https://translate.google.com/?#id/id')


# In[7]:


s_iface = start_iface()


# In[8]:


time.sleep(4)
debug = True


# In[9]:


cipi_recognized = False
ear.debug = False
feature_dim_1 = 20
feature_dim_2 = 11
channel=1

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
            rec_speech(s_iface)
            ear.debug = False
            ear.start(thres=800, timeout=5, process=transcrib)
            if speech != "": 
                
                #RANDOMIZE THIS
                playdetected()
                reply, humanstate, botstate = sequence(speech, humanstate, botstate)
                talk_until_complete(reply,s_iface)
            else:
                speech = " "
                att_counter += 1
                if att_counter > 1:
                    att_counter = 0
                    cipi_recognized = False
                    attention = False
                    
                    #RANDOMIZE THIS
                    playehm()
                    time.sleep(2)
                    print("\n=============\nGo to wait mode")

