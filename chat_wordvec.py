import nltk
import re
import gensim
import numpy as np


w2vmodel="./model/chat_model1-300.w2v"   #filename
num_features = 300    #number of features in the model
maxsent = 10          #maximum words in a sentence.
intent=[]

tex2vec =  gensim.models.KeyedVectors.load(w2vmodel)

def remove_unchar(flist):
    try:
        flist.remove("?")
    except:
        pass

def twl(sentence, rempunct=True, flat=True):
    """Tokenize word dari sebuah sentence/kalimat"""
    if not flat:
        sntoken = nltk.sent_tokenize(sentence)
    else:
        sntoken = [sentence]
    for i in range(len(sntoken)):
        tokens = nltk.word_tokenize(sntoken[i])
        if rempunct==True:
            type(tokens)
            text = nltk.Text(tokens)
            type(text)  
            sntoken[i] = [w.lower() for w in text if w.isalpha()]
        else: sntoken[i] = tokens
    if len(sntoken)==1: 
        sntoken = sntoken[0]
        remove_unchar(sntoken)
    for i in sntoken:
        remove_unchar(i)
    if sntoken==[]: sntoken=['yang']
    #print(sntoken)
    return sntoken

def zerolistmaker(n):
    """Membuat list berisi 0, mirip seperti np.zeros"""
    listofzeros = [1] * n
    return listofzeros

def swv_ar(sentence, maxword=maxsent, vecsize=num_features, frontpad=True):
    """Sentence word2vec to array matrices for processing"""
    senarray=[]
    if len(sentence)>=maxsent: 
        print("Sentence overflow:",sentence)
        sentence=sentence[0:maxsent-1]
    if type(sentence[0])==list:
        for i in range(len(sentence)):
            for k in range(len(sentence[i])):
                #print(tex2vec[sentence[i][k]])
                try:
                    senarray.append(tex2vec[sentence[i][k]])
                except Exception as e:
                    print("Problem at phrase:", sentence[i][k])
                    
    else:
        for i in range(len(sentence)):
            try:
                senarray.append(tex2vec[sentence[i]])
            except Exception as e:
                print("Problem at phrase:", sentence[i])
                
    zr=zerolistmaker(num_features)
    #reverse if want to add a padding in front
    if frontpad: senarray.reverse()

    #add the padding
    for i in range(maxword-len(senarray)):     
        senarray.append(zr)

    #reverse again
    if frontpad: senarray.reverse()            
    
    return np.array(senarray)

def wv_ts(array, weight=False):
    """Wave2vec matrix to sentence - weight untuk menampilkan bobot"""
    result=[]
    for i in array:
        try:
            word=tex2vec.similar_by_vector(vector=i,topn=1)
            if word[0][1] == 0: word[0]="."
                
            #bikin yang mau di append ada bobotnya gak?
            if weight == False:
                to_app = word[0][0]
            else: to_app = word[0]
                
            result.append(to_app)
        except:
            pass
    return result

def read_ar(filename, start=0, lines=10):
    """Membaca file lalu merubahnya menjadi sebuah matrix secara per baris"""
    resl = []
    res = []
    with open(filename,"r",encoding="utf8") as f:
        #lines to skip
        for i in range(0,start):
            f.readline()
        #selecting begin here
        for i in range(0,lines):
            resl.append(f.readline())
    f.close()
    
    for i in range(len(resl)):
        #debugging what is read
        #print(resl[i])
        fl = swv_ar(twl(resl[i],rempunct=True,flat=True))
        #print(res.shape)
        res.append(fl)
    return np.array(res)
