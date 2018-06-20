import selenium
import time
import soundfile
import sounddevice
from selenium import webdriver

headless = False

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
if headless:
    chrome_options.add_argument("--headless")  
   

def cek_talk_or_speak(s_iface):
    try:
        m = s_iface.find_element_by_class_name("goog-toolbar-button-checked")
        return True
    except:
        return False

def get_speech(s_iface):
    if not cek_talk_or_speak(s_iface):
        try:
            record = s_iface.find_element_by_xpath('//*[@id="gt-speech"]/span')
            record.click()
            time.sleep(4)
            #record
            record.click()
            source = s_iface.find_element_by_xpath('//*[@id="source"]')
            a = source.get_attribute("value")
            clear(s_iface)
            playding()
        except:
            del s_iface
            start_iface()
            talk("maaf ada kesalahan, coba lagi",s_iface)
            record = s_iface.find_element_by_xpath('//*[@id="gt-speech"]/span')
            record.click()
            time.sleep(4)
            #record
            record.click()
            source = s_iface.find_element_by_xpath('//*[@id="source"]')
            a = source.get_attribute("value")
            clear(s_iface)
            playding()
    return a

def clear(s_iface):
    source = s_iface.find_element_by_xpath('//*[@id="source"]')
    source.clear()
    
def talk(speech, s_iface):
    if not cek_talk_or_speak(s_iface):
        try:
            tts = s_iface.find_element_by_xpath('//*[@id="source"]')
            time.sleep(0.2)
            tts.clear()
            time.sleep(0.5)
            tts.send_keys(str(speech))
            time.sleep(1)

            talk = s_iface.find_element_by_id('gt-res-listen') 
            talk.click()
            time.sleep(1)
        except:
            del s_iface
            start_iface()

            tts = s_iface.find_element_by_xpath('//*[@id="source"]')
            tts.clear()
            time.sleep(0.5)
            tts.send_keys("Maaf ada kesalahan, coba ulangi lagi")
            time.sleep(1)

            talk = s_iface.find_element_by_id('gt-res-listen') 
            talk.click()
            time.sleep(1)
            

def check_live(s_iface):
    try:
        result=s_iface.execute_script("return document.readyState;")
        return True
    except:
        return False

def playding():
    wv,sr = soundfile.read("./ehm.wav")
    sounddevice.play(wv,samplerate=44100)

def playya():
    wv,sr = soundfile.read("./ya.wav")
    sounddevice.play(wv,samplerate=44100)
