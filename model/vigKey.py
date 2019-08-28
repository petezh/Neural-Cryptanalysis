# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 19:31:57 2019

@author: patri
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import pickle

labels = []
datas = []
load = pickle.load(open('vigenereCiphers.obj','rb'))
li = []
percent = 0.7
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
for a in load:
    x = len(a[0])
    y = autocorrelate(a[1])
    labels.append(x)
    datas.append(y)
    li.append([x,y])
for i in range(0,len(datas)):
    datas[i] = np.true_divide(datas[i], np.amax(datas[i]))
model = keras.Sequential()
model.add(keras.layers.Dense(21, activation=tf.nn.relu))
model.add(keras.layers.Dense(21, activation=tf.nn.sigmoid))
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
c = int(percent*len(datas))
model.fit(np.array(datas[:c]), np.array(labels[:c]), epochs=10, batch_size = 32)
dfsdf = model.evaluate(np.array(datas[c:]),np.array(labels[c:]))

