# -*- coding: utf-8 -*-
"""
Created on Sun May 27 14:53:14 2018

@author: Admin
"""
import nltk

fs=open("dialog_simple","r",encoding="utf8").readlines()
tlen=300

res = []
lf = []
wc = 0
rl = 0
fn = 1
for i in range(len(fs)):
    rl += 1
    wc = wc + len(nltk.word_tokenize(fs[i]))
    if wc>5000:
        print("line exceed 5000")
    res.append(fs[i])
    if rl == 300:
        fnm = str(fn)+".inp"
        with open(fnm,"w") as f:
            for i in range(len(res)):
                f.writelines(res[i])
        print("Write file:",fnm)
        fn += 1
        rl=0
        wc=0

        
        
    

