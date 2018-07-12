import selenium
import time
import soundfile
import sounddevice
from selenium import webdriver
import asyncio
import logging

headless = False

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
if headless:
    chrome_options.add_argument("--headless")  
   

def tlk_or_spk_isactive(s_iface):
    """CHECKING-if true the bot is still talking"""
    try:
        m = s_iface.find_element_by_class_name("goog-toolbar-button-checked")
        logging.debug("NOT ERROR- Got the button active")
        return True
    except Exception as e:
        logging.debug("ERROR- Cannot get tlk_or_spk_isactive result")
        return False


    
def rec_speech(s_iface):
    """First click for recording a speech in selenium"""
    if not tlk_or_spk_isactive(s_iface):
        try:
            record = s_iface.find_element_by_xpath('//*[@id="gt-speech"]/span')
            record.click()
            time.sleep(0.5)
        except Exception as e:
            logging.error("ERROR- Cannot execute rec_speech(s_iface)")
            pass

def transcribe_speech(s_iface):
    """Click to Stop recognizer - and Get the result"""
    if tlk_or_spk_isactive(s_iface):
        try:
            time.sleep(0.1)
            record = s_iface.find_element_by_xpath('//*[@id="gt-speech"]/span')
            record.click()
            time.sleep(0.1)
            source = s_iface.find_element_by_xpath('//*[@id="source"]')
            a = source.get_attribute("value")
            time.sleep(0.1)
            clear(s_iface)
            logging.debug("retrieved Speech:"+str(a))
        except:
            logging.error("ERROR- Cannot execute transcribe_speech(s_iface)")
            a = "halo"
        return a

def clear(s_iface):
    """Clear - the field of speech"""
    try:
        source = s_iface.find_element_by_xpath('//*[@id="source"]')
        source.clear()
    except Exception as e:
        logging.error("ERROR- Cannot clear speech textbox")
    
def talk(speech, s_iface):
    """Basic Talking no need to check"""
    global talking
    talking = True
    try:
        tts = s_iface.find_element_by_xpath('//*[@id="source"]')
        asyncio.sleep(0.05)
        time.sleep(0.05)
        tts.clear()
        asyncio.sleep(0.1)
        time.sleep(0.1)
        tts.send_keys(str(speech))
        logging.debug("Talk:"+str(speech))
        asyncio.sleep(0.5)
        time.sleep(0.5)
        logging.debug("Talk this:"+speech)
        talk = s_iface.find_element_by_id('gt-res-listen') 
        talk.click()
        asyncio.sleep(1)
        time.sleep(1)
        
    except:
        logging.error("Tried to talk:",str(speech))
        logging.error("ERROR- Cannot run talk(speech,s_iface)")
        playerror()
        asyncio.sleep(1)

def talk_until_complete(sentence, s_iface):
    """More safe click to talk button"""
    try:
        counter=0
        global talking
        talking = True
        logging.debug("Try talk_until_complete:"+str(sentence))
        talk(sentence, s_iface)
        while talking:
            if not tlk_or_spk_isactive(s_iface):
                talking=False
                #print('X')
                asyncio.sleep(0.1)
                time.sleep(0.2)
                clear(s_iface)
            else:
                #print("_",end='')
                counter += 1
                asyncio.sleep(0.02)
                if counter > (80 * 10):
                    clear(s_iface)
                    playya()
                    transcribe_speech(s_iface)
    except Exception as e:
        logging.error("Tried to talk:"+str(sentence))
        logging.error("ERROR- Cannot run talk_until_complete:"+str(e))

def check_live(s_iface):
    """ Check if s_iface exists and can run """
    try:
        result=s_iface.execute_script("return document.readyState;")
        return True
    except Exception as e:
        logging.error("ERROR- Cannot run check_live:"+str(e))
        return False

def playehm():
    """Suara cipi ehm"""
    wv,sr = soundfile.read("./ehm.wav")
    sounddevice.play(wv,samplerate=44100)

def playya():
    """Bilang ya"""
    wv,sr = soundfile.read("./ya.wav")
    sounddevice.play(wv,samplerate=44100)

def playdetected():
    """Bunyi apabila hotword di detect"""
    wv,sr = soundfile.read("./Ring09.wav")
    sounddevice.play(wv,samplerate=44100)
    
def playerror():
    """Bilang kalau ada kesalahan internal"""
    wv, sr = soundfile.read("./error.wav")
    sounddevice.play(wv,samplerate=44100)

def playerror_internet():
    """ Bilang kalau tidak ada internet"""
    wv, sr = soundfile.read("./error_internet.wav")
    sounddevice.play(wv,samplerate=44100)
