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

    
data = pd.read_csv("affpairs.csv").values
labels = []
datas = []
a = [1,3,5,7,9,11,15,17,19,21,23,25]

#what portion of the data to use as training
percent = 0.8

#formatting
for i in range(0,len(data)):
    if (data[i][1]%26) in a:
        labels.append(int(((data[i][0]-1)%26)*12+a.index(data[i][1]%26)))
        datas.append(data[i][2:])
#normalize to [0,1] frequencies
for i in range(0,len(datas)):
    datas[i] = np.true_divide(datas[i], np.sum(datas[i]))
model = keras.Sequential()
model.add(keras.layers.Dense(12, activation=tf.nn.relu))
model.add(keras.layers.Dense(26, activation=tf.nn.relu))
model.add(keras.layers.Dense(312, activation=tf.nn.sigmoid))
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
numTest = round(len(datas)*percent)
trial_data = datas[:numTest]
test_data = datas[numTest:]

trial_labels = labels[:numTest]
test_labels = labels[numTest:]
#8523 in caepairs.csv
#test it, first 6000 5 times through, test around 2500
model.fit(np.array(trial_data), np.array(trial_labels), epochs=150, batch_size = 32)
dfsdf = model.evaluate(np.array(test_data),np.array(test_labels))
print(dfsdf)
