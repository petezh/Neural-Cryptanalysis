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
from math import sqrt

data = pd.read_csv("hillpairsnxn.csv").values
labels = []
datas = []

percent = 0.8
#formatting
n = round(sqrt(len(data[0])-26))
for i in range(0,len(data)):
    zero = [0]*(26*n*n)
    for j in range(n*n):
        zero[data[i][j] + j*26] = 1
    labels.append(zero)
    datas.append(data[i][n*n:])
#normalize to [0,1] frequencies
for i in range(0,len(datas)):
    datas[i] = np.true_divide(datas[i], np.sum(datas[i]))
model = keras.Sequential()
model.add(keras.layers.Dense(26, activation=tf.nn.sigmoid))
model.add(keras.layers.Dense(26*n*n, activation=tf.nn.sigmoid))
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
numTest = int(len(datas)*percent)
numTest = 5000
trial_data = datas[:numTest]
test_data = datas[numTest:]

trial_labels = labels[:numTest]
test_labels = labels[numTest:]
#8523 in caepairs.csv
#test it, first 6000 5 times through, test around 2500
model.fit(np.array(trial_data), np.array(trial_labels), epochs=5, batch_size = 16)
dfsdf = model.evaluate(np.array(test_data),np.array(test_labels))
print(dfsdf)