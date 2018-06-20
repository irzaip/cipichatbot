import webbrowser
from flask import Flask
from pyautogui import alert
from selenium import webdriver

headless=False

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
if headless:
    chrome_options.add_argument("--headless")  


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/web')
def webbrowse():
    webbrowser.open("www.detik.com")
    return "Done"

@app.route('/alert')
def alertme():
    rd = alert(text='Realy close this app?', title='REQUEST', button='OK', timeout=5000)
    return rd


@app.route('/create')    
def start_iface():
    global s_iface
    s_iface = webdriver.Chrome(chrome_options=chrome_options)
    s_iface.get('https://translate.google.com/?#id/id')
    assert "Google Translate" in s_iface.title
    return "OK"
    
@app.route('/close')
def close():
    s_iface.close()
    return "OK"