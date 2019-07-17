# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 08:34:47 2019

@author: patri AND PETER
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

import re
import csv
import random
import string
import multiprocessing
import itertools

frequencies = []

def main():

    caesar_train(2, "span")

def caesar_train(length, lang):

    yield "Setting up model..."
    
    data = pd.read_csv(lang + '_' + str(length) + 'cea.csv').values
    labels = []
    datas = []
    #formatting
    for i in range(0,len(data)):
        labels.append((data[i][0]-1)%26)
        datas.append(data[i][1:])
    #normalize to [0,1] frequencies
    for i in range(0,len(data)):
        datas[i] = np.true_divide(datas[i], np.sum(datas[i]))
    #create model
    model = keras.Sequential()
    model.add(keras.layers.Dense(26, activation=tf.nn.sigmoid))
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    trial_data = datas[:50000]
    test_data = datas[50000:]

    trial_labels = labels[:50000]
    test_labels = labels[50000:]
    #8523 in caepairs.csv
    #test it, first 6000 5 times through, test around 2500
    yield 'Training model...'
    model.fit(np.array(trial_data), np.array(trial_labels), epochs=10, batch_size = 32)
    yield 'Training complete. Testing model...'
    results = model.evaluate(np.array(test_data),np.array(test_labels))
    neuralAcc = results[1]
    yield 'Testing complete. Accuracy: %f' % neuralAcc
    
       
    if __name__ == '__main__':
        dotAcc = test_all(length, lang)

        fd = csv.writer(open('results.csv','a'), lineterminator = "\n")
        fd.writerow([lang, length, neuralAcc, dotAcc])
        

## DOT PRODUCT TESTING

def test(data, freq):
    dot = []
    for x in range(0,26):
        shift = data.tolist()[x:] + data.tolist()[:x]
        dot.append(np.dot(np.array(freq),np.array(shift)))
    return dot.index(max(dot))

def test_all(length, lang):
    path = lang + '_' + str(length) + 'cea.csv'
    data = pd.read_csv(path).values

    if lang == "eng":
        letterfreq ={'E' : 12.0, 'T' : 9.10, 'A' : 8.12, 'O' : 7.68, 'I' : 7.31, 'N' : 6.95, 'S' : 6.28, 'R' : 6.02, 'H' : 5.92, 'D' : 4.32, 'L' : 3.98, 'U' : 2.88, 'C' : 2.71, 'M' : 2.61, 'F' : 2.30, 'Y' : 2.11, 'W' : 2.09, 'G' : 2.03, 'P' : 1.82, 'B' : 1.49, 'V' : 1.11, 'K' : 0.69,'X' : 0.17, 'Q' : 0.11, 'J' : 0.10, 'Z' : 0.07 }

    if lang=="span":
        letterfreq ={'E' : 13.72, 'A' : 11.72, 'O' : 8.44, 'S' : 7.2, 'N' : 6.83, 'R' : 6.41, 'I' : 5.28, 'L' : 5.24, 'D' : 4.67, 'T' : 4.6, 'U' : 4.55, 'C' : 3.87, 'M' : 3.08, 'P' : 2.89, 'B' : 1.49, 'H' : 1.18, 'Q' : 1.11, 'Y' : 1.09, 'V' : 1.05, 'G' : 1, 'F' : 0.69, 'J' : 0.52, 'Z' : 0.47, 'X' : 0.14, 'K' : 0.11, 'W' : 0.04}

    if lang=="fren":
        letterfreq ={'A' : 7.6, 'B' : 0.96, 'C' : 3.39, 'D' : 4.08, 'E' : 14.47, 'F' : 1.12, 'G' : 1.18, 'H' : 0.93, 'I' : 7.21, 'J' : 0.3, 'K' : 0.16, 'L' : 5.86, 'M' : 2.78, 'N' : 7.32, 'O' : 5.39, 'P' : 2.98, 'Q' : 0.85, 'R' : 6.86, 'S' : 7.98, 'T' : 7.11, 'U' : 5.55, 'V' : 1.29, 'W' : 0.08, 'X' : 0.43, 'Y' : 0.34, 'Z' : 0.10} 
            
    let = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    frequencies = []
    
    for x in let:
        frequencies.append(round(letterfreq[x]/100,4))
    
    labels = []
    datas = []
    for i in range(0,5000):
        labels.append((data[i][0])%26)
        datas.append(data[i][1:])

    #normalize to [0,1] frequencies

    for i in range(0,5000):
        datas[i] = np.true_divide(datas[i], np.sum(datas[i]))
    x = [test(y, frequencies) for y in datas]
    count = [(y == z) for y,z in zip(x,labels)]
    count = sum(count)
    print(count/5000)
    return count/5000

if __name__ == "__main__":
    main()
