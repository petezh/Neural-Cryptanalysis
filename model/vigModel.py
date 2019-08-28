# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:59:09 2019

@author: patri
"""
import tensorflow as tf
import pickle
import numpy as np
from tensorflow import keras

alpha = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
caesar = keras.models.load_model('caesarModel.h5')
vigenere = keras.models.load_model('keyLengthModel.h5')

load = pickle.load(open('vigenereCiphers.obj','rb'))

def autocorrelate(a): #create autocorrelation counts for 
    n = 20 #maximum length of key
    n *= 10
    li = [0]
    for x in range(1,n):
        corr = 0
        shift = a[x:]
        for i in range(len(shift)):
            if shift[i] == a[i]:
                corr += 1
        li.append(corr)
    li[0] = max(li)
    return li
def frequency(text):

    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    freq = list()
    
    for i in range(26):
        freq.append(text.count(alpha[i]))
    return freq
training = [autocorrelate(a[1]) for a in load]
keys = [a[0] for a in load]
cipherText = [a[1] for a in load]
for i in range(0,len(training)):
    training[i] = np.true_divide(training[i], np.amax(training[i]))
keyLengths = vigenere.predict(np.array(training))
keyLengths = [a.argmax() for a in keyLengths]
correct = 0
for i in range(len(training)):
    correctKey = keys[i]
    keysss = []
    for j in range(keyLengths[i]):
        cipher = cipherText[i][j::keyLengths[i]]
        keysss.append(frequency(cipher))
    #train caesar on it
    for i in range(0,len(keysss)):
        keysss[i] = np.true_divide(keysss[i], np.sum(keysss[i]))
    keysss = caesar.predict(np.array(keysss))
    keysss = [a.argmax() for a in keysss]
    keysss = ''.join([alpha[a] for a in keysss])
    if keysss == correctKey:
        correct += 1
print('correct: ' + str(correct) +' of ' + str(len(training)))
print(float(correct)/float(len(training)))