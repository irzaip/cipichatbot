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
import re
import datetime

def input(sentence):
    reply={'intent': 'jam','name':'None','followup': 'None','prompt': 'oke'}    
    #kalau entities sudah lengkap. lekas proses
    hour=datetime.datetime.now().hour
    minutes=datetime.datetime.now().minute
    if hour > 12:
        hour = hour - 12

    reply['prompt']="sekarang jam, "+str(hour)+":"+str(minutes)
    #print(reply)
    return reply

def process():
    print("affirm")
    pass
    
    #RESET BY LOADING AGAIN THE YAML FILE

datetime.datetime.now().hour
if __name__ == '__main__':
	input("lihat gambar")