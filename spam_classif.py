import codecs
import json
import os
import re
import nltk
import numpy as np
from operator import itemgetter
 
def read_tr(dir):
    data1 = []
    way_tr = []
    for file in os.listdir(dir):        
        with codecs.open(os.path.join(dir, file), 'r', 'utf-8') as f:
            data1.append(json.load(f))       
            way_tr.append(file)     
    return data1, way_tr

def read_mn(dir):
    data2 = []
    way_mn = []
    for file in os.listdir(dir):
        with codecs.open(os.path.join(dir, file), 'r', 'utf-8') as f:
            data2.append(json.load(f))
            way_mn.append(file)
    return data2, way_mn
    
data_tr = read_tr('/home/partizan/classif2/spam_data/train')
data_mn, way_mn = read_mn('/home/partizan/classif2/spam_data/test')

def read_povt():
    f = open("words.txt", "r")
    text = nltk.word_tokenize(f.read())
    povt_mass = []
    for i in text:
        povt_mass.append(i)
    return povt_mass

def train(data_tr, way_tr, data_mn, way_mn, povt_mass):
    n = 0
    m = 0
    vect_tr = []
    vect_mn = []
    while n < len(data_tr):
          a = [0 for i in xrange(50)]
          a.append(data_tr[n]['is_spam'])
          vect_tr.append(a)
          tokens = nltk.word_tokenize(data_tr[n]['subject'])         
          while m < len(povt_mass):
                vect_tr[n][m] = tokens.count(povt_mass[m])
                m = m + 1
          m = 0                
          n = n + 1  
    n = 0 
    m = 0
    while n < len(data_mn):
          a = [0 for i in xrange(50)]
          a.append(way_mn[n])
          vect_mn.append(a)
          tokens = nltk.word_tokenize(data_mn[n]['subject']) 
          while m < len(povt_mass):
                vect_mn[n][m] = tokens.count(povt_mass[m])
                m = m + 1
          m = 0              
          n = n + 1  
    return vect_tr, vect_mn 

def classif(vect_tr, vect_mn):
    f = open('test.txt','w')
    n = 0
    m = 0
    c = 0
    sum = 0
    long_mass = []
    while n < len(vect_mn):
      while m < len(vect_tr):
        while c != 50:
          koaf = ((vect_tr[m][c]-vect_mn[n][c])**2)
          sum = koaf + sum
          c = c + 1
        sqr = np.sqrt(sum)
        c = 0
        long_mass.append([sqr, vect_tr[m][50]])
        #
        sum = 0
        koaf = 0
        m = m + 1
      print n
      long_mass = sorted(long_mass, key=itemgetter(0))
      vsp_mass = []
      d = 0
      while d < 20:
        vsp_mass.append(long_mass[d][1])
        d = d + 1
      d = 0
      if vsp_mass.count(False) >= vsp_mass.count(True):
        f.write(u'%s\t%s\n' % (way_mn[n], False))
      else:
        f.write(u'%s\t%s\n' % (way_mn[n], True))
      vsp_mass = []
      long_mass = []
      sum = 0
      n = n + 1
      m = 0
    
    f.close()

data_tr, way_tr = read_tr('/home/partizan/classif2/spam_data/train')
data_mn, way_mn = read_mn('/home/partizan/classif2/spam_data/test')

vect_tr, vect_mn = train(data_tr, way_tr, data_mn, way_mn, read_povt())
classif(vect_tr, vect_mn)

