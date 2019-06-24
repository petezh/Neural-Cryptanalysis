# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 08:34:47 2019

@author: patri
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #some visuals, dont need in program

def str_to_list(s):
    return [int(x) for x in s[1:len(s)-1].split(', ')]
    
data = pd.read_csv("caepairs.csv")
labels = []
datas = []
#formatting
for i in range(0,len(data.index)):
    labels.append((data.loc[i][0]-1)%26)
    datas.append(str_to_list(data.loc[i][1]))
#normalize to [0,1] frequencies
for i in range(0,len(datas)):
    for j in range(0,26):
        datas[i][j] /= sum(datas[i])
model = keras.Sequential()
model.add(keras.layers.Dense(26, activation=tf.nn.relu))
model.add(keras.layers.Dense(26, activation=tf.nn.sigmoid))
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
trial_data = datas[:6000]
test_data = datas[6000:]

trial_labels = labels[:6000]
test_labels = labels[6000:]
#8523 in caepairs.csv
#test it, first 6000 5 times through, test around 2500
model.fit(np.array(trial_data), np.array(trial_labels), epochs=5, batch_size = 32)
dfsdf = model.evaluate(np.array(test_data),np.array(test_labels))
print(dfsdf)
input()