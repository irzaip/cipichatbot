# conversation-flow : v.0.01
# template by Irza Pulungan
# todo:
# memparsing hasil response lalu di cocokkan dengan type
import keras
import os
import time
#from ..module import rontok
import yaml
import os
import re
from chat_wordvec import *

cmodel = keras.models.load_model("./model/chitchat-300-1.mdl")

maxsent=50
num_features = 300

import pickle
respons = pickle.load(open('respons.p','rb'))
integer_encoded = pickle.load(open('integer_encoded.p','rb'))
onehot_encoded = pickle.load(open('onehot_encoded.p','rb'))


def input(sentence):
    
    #reply={'name': 'None', 'followup': 'None', 'prompt': 'gak ngerti'}
    #kalau entities sudah lengkap. lekas proses

    """memprediksi masuk intent apakah sebuah kalimat."""
    sentence_vectorized=np.array([swv_ar(twl(sentence,rempunct=True,flat=True),maxword=maxsent, vecsize=num_features)])
    predictions=cmodel.predict(sentence_vectorized)
    cls_pred = np.argmax(predictions,axis=1)
    #print(predictions)
    
    #ini sangat tricky -> dari prediksi balikkan ke integer_encodednya dulu baru 
    #cari ke indexnya dari response
    
    jawaban = respons[list(integer_encoded).index(cls_pred[0])]

    reply={'name': 'None', 'followup': 'None', 'prompt': jawaban , 'score': predictions.max(), 'sentence': sentence, 'cls:': cls_pred}
    return reply

def process():
    print("chitchat")
    pass
    
    #RESET BY LOADING AGAIN THE YAML FILE


if __name__ == '__main__':
	input("chitchat")