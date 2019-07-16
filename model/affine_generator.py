"""
a port of affine.py that allows for interfacing with the GUI

@author: evan
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
from tensorflow.keras.utils import to_categorical

def train(length, lang):
    yield "Setting up model..."
    dataPath = 'affpairs.csv'
    data = pd.read_csv(dataPath).values
    labels = []
    datas = []
    a = [1,3,5,7,9,11,15,17,19,21,23,25]
    
    percentage = 0.8
    
    #formatting
    for i in range(0, len(data)):
        if (data[i][1] % 26) in a:
            labels.append(int(((data[i][0]-1)%26)*12+a.index(data[i][1]%26)))
            datas.append(data[i][2:])
    #normalize to [0, 1] frequencies
    for i in range(0, len(datas)):
        datas[i] = np.true_divide(datas[i], np.sum(datas[i]))
    model = keras.Sequential()
    model.add(keras.layers.Dense(12, activation=tf.nn.relu))
    model.add(keras.layers.Dense(26, activation=tf.nn.relu))
    model.add(keras.layers.Dense(312, activation=tf.nn.sigmoid))
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    numTest = round(len(datas)*percentage)
    trial_data = datas[:numTest]
    test_data = datas[numTest:]

    trial_labels = labels[:numTest]
    test_labels = labels[numTest:]

    yield "Training model..."
    model.fit(np.array(trial_data), np.array(trial_labels), epochs=150, batch_size = 32)
    yield "Training complete. Testing model..."
    results = model.evaluate(np.array(test_data),np.array(test_labels))
    yield "Testing complete. Accuracy: %f" % results[1]
