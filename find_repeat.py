import codecs
import json
import os
import re
import nltk
from operator import itemgetter
 
def read_tr(dir):
    data1 = []
    way_tr = []
    for file in os.listdir(dir):        
        with codecs.open(os.path.join(dir, file), 'r', 'utf-8') as f:
            data1.append(json.load(f))          
    return data1
    
data_tr = read_tr('/home/partizan/classif2/spam_data/train')

def fnd_repeat(data_tr):
    n = 0
    vect_tr = []
    main_data = []
    while n < len(data_tr):
          if (data_tr[n]['is_spam'] == True):
              main_data = nltk.word_tokenize(data_tr[n]['subject']) + main_data
          print n
          n = n + 1
    vect_povt = []  
    vect_1 = []   
    for i in main_data:
        try:
           vect_1.index(i)
        except:
           vect_povt.append([main_data.count(i), i])
           vect_1.append(i)
    vect_povt = sorted(vect_povt, key=itemgetter(0))
    vect_povt = reversed(vect_povt)
    print vect_povt
    f = open("words.txt", "w")
    n = 0
    for i in vect_povt:
        if n != 50:
           f.write(i[1] + " " + "\n")
           n = n + 1
        else: break

fnd_repeat(data_tr)
