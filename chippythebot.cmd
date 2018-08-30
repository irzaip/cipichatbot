@echo off

CLS
e:
SET PY_HOME=C:\Anaconda3\
SET PYTHONPATH=e:\data\python\3.6\Words\cipichatbot\;.



cd e:\data\python\3.6\Words\cipichatbot\


c:\Anaconda3\Scripts\pip install tensorflow keras tqdm sounddevice soundfile librosa Sastrawi selenium gensim
c:\anaconda3\python Cipi-theChatbot.py

REM c:\anaconda3\python 

pause


