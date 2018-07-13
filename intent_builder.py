import glob
import fileinput
import yaml
import importlib
import logging

fls = glob.glob('./data/*/input.txt')
intent = []
prep_x = []
prep_y = []
for i in fls:
    for tx in fileinput.input(i):
        intent.append(i.split('\\')[-2])
fileinput.close()

intent = list(set(intent))
intent.sort()
print(intent)

min_pred={}

#loader all intent
for i in intent:
    exect = 'from data.'+i+" import "+i
    #exect = f"importlib.import_module('data.{i}')"
    try:
        exec(exect)
        print(exect)
    except:
        logging.error("Error loading:"+str(exect))
    
    min_pred[i] = 0.1

a = glob.glob('./data/*/*.yml')
for i in a:
    with open(i, 'r') as f:
        fi = f.read()
    min_pred[yaml.load(fi)['intent']] = yaml.load(fi)['min_score']
