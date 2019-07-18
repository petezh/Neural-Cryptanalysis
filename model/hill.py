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
from tensorflow.keras.utils import to_categorical

    
data = pd.read_csv("hillpairs2x2.csv").values
labels = []
datas = []

percent = 0.8
#formatting
for i in range(0,len(data)):
    zero = [0]*(26*4)
    zero[data[i][0]]=1
    zero[data[i][1]+26]=1
    zero[data[i][2]+52]=1
    zero[data[i][3]+78]=1
    labels.append(zero)
    datas.append(data[i][4:])
#normalize to [0,1] frequencies
for i in range(0,len(datas)):
    datas[i] = np.true_divide(datas[i], np.sum(datas[i]))
model = keras.Sequential()
model.add(keras.layers.Dense(26, activation=tf.nn.sigmoid))
model.add(keras.layers.Dense(26, activation=tf.nn.sigmoid))
model.add(keras.layers.Dense(26, activation=tf.nn.sigmoid))
model.add(keras.layers.Dense(26, activation=tf.nn.sigmoid))
model.add(keras.layers.Dense(26*4, activation=tf.nn.sigmoid))
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
numTest = int(len(datas)*percent)
print(numTest)
trial_data = datas[:numTest]
test_data = datas[numTest:]

trial_labels = labels[:numTest]
test_labels = labels[numTest:]
#8523 in caepairs.csv
#test it, first 6000 5 times through, test around 2500
model.fit(np.array(trial_data), np.array(trial_labels), epochs=5, batch_size = 16)
dfsdf = model.evaluate(np.array(test_data),np.array(test_labels))
print(dfsdf)