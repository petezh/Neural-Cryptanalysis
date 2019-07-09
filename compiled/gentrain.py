# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 08:34:47 2019

@author: patri AND PETER
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #some visuals, dont need in program

import re
import csv
import random
import string
import multiprocessing
import itertools

frequencies = []

def main():

    languages = ["eng", "span", "fren"]
    lengths = [1, 2, 3]
    for length in lengths:
        for language in languages:
            print("Training length " + str(length) + " on langauge " + language + ".")
            train(length, language)

def train(length, lang):



    
    wordList = eval(next(open(lang + "_alltext.txt", 'r')))
    
    
    # define output file
    snipOut = open(lang + "snip" + str(length) + '.txt', 'w')

    snippet = ""
    counter = 0
    nosnips = 0

    # make word snippets
    for word in wordList:
        
        snippet = snippet + str(word)
        counter = counter + 1
        if counter==length:

            # write to file in all upper
            snippet = re.sub(r'[^a-zA-Z ]+', '', snippet)
            snipOut.write(snippet.upper()+"\n")
            counter = 0
            snippet = ""
            nosnips = nosnips+1

    print("Cut "+str(nosnips) + " snips.")
    
    snipOut.close()
    

    snippets = open(lang + "snip" + str(length) + '.txt', 'r')
    caefile = open(lang + '_' + str(length) + 'cea.csv','w')
    caewtr = csv.writer(caefile, lineterminator = "\n")
    caewtr.writerow(['shift'] + [char for char in string.ascii_uppercase])


    
    for snip in snippets:

        snip = re.sub("[^a-zA-Z]+", '', snip)
        
        
        # make caesar pairs
        shift = random.randint(1, 26)
        ciphertext = caesar(snip, shift)
        freq = frequency(ciphertext)
        caewtr.writerow([shift] + freq)
    caefile.close()
    print("Generated caesar ciphertexts.")
    
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
    model.fit(np.array(trial_data), np.array(trial_labels), epochs=10, batch_size = 32)
    dfsdf = model.evaluate(np.array(test_data),np.array(test_labels))
    neuralAcc = dfsdf[1]
    


    if lang == "eng":
        letterfreq ={'E' : 12.0, 'T' : 9.10, 'A' : 8.12, 'O' : 7.68, 'I' : 7.31, 'N' : 6.95, 'S' : 6.28, 'R' : 6.02, 'H' : 5.92, 'D' : 4.32, 'L' : 3.98, 'U' : 2.88, 'C' : 2.71, 'M' : 2.61, 'F' : 2.30, 'Y' : 2.11, 'W' : 2.09, 'G' : 2.03, 'P' : 1.82, 'B' : 1.49, 'V' : 1.11, 'K' : 0.69,'X' : 0.17, 'Q' : 0.11, 'J' : 0.10, 'Z' : 0.07 }

    if lang=="span":
        letterfreq ={'E' : 13.72, 'A' : 11.72, 'O' : 8.44, 'S' : 7.2, 'N' : 6.83, 'R' : 6.41, 'I' : 5.28, 'L' : 5.24, 'D' : 4.67, 'T' : 4.6, 'U' : 4.55, 'C' : 3.87, 'M' : 3.08, 'P' : 2.89, 'B' : 1.49, 'H' : 1.18, 'Q' : 1.11, 'Y' : 1.09, 'V' : 1.05, 'G' : 1, 'F' : 0.69, 'J' : 0.52, 'Z' : 0.47, 'X' : 0.14, 'K' : 0.11, 'W' : 0.04}

    if lang=="fren":
        letterfreq ={'A' : 7.6, 'B' : 0.96, 'C' : 3.39, 'D' : 4.08, 'E' : 14.47, 'F' : 1.12, 'G' : 1.18, 'H' : 0.93, 'I' : 7.21, 'J' : 0.3, 'K' : 0.16, 'L' : 5.86, 'M' : 2.78, 'N' : 7.32, 'O' : 5.39, 'P' : 2.98, 'Q' : 0.85, 'R' : 6.86, 'S' : 7.98, 'T' : 7.11, 'U' : 5.55, 'V' : 1.29, 'W' : 0.08, 'X' : 0.43, 'Y' : 0.34, 'Z' : 0.10} 
            
    let = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    global frequencies
    frequencies = []
    
    for x in let:
        frequencies.append(round(letterfreq[x]/100,4))

    dotAcc = test_all(lang + '_' + str(length) + 'cea.csv')

    fd = csv.writer(open('results.csv','a'), lineterminator = "\n")
    fd.writerow([lang, length, neuralAcc, dotAcc])

## DOT PRODUCT TESTING

def test(data):
    dot = []
    for x in range(0,26):
        shift = data.tolist()[x:] + data.tolist()[:x]
        dot.append(np.dot(np.array(frequencies),np.array(shift)))
    return dot.index(max(dot))

def test_all(path):
    data = pd.read_csv(path).values
    labels = []
    datas = []
    for i in range(0,5000):
        labels.append((data[i][0])%26)
        datas.append(data[i][1:])

    #normalize to [0,1] frequencies

    for i in range(0,5000):
        datas[i] = np.true_divide(datas[i], np.sum(datas[i]))
    x = [test(y) for y in datas]
    count = [(y == z) for y,z in zip(x,labels)]
    count = sum(count)
    print(count/5000)
    return count/5000


### UTILITIES FOR GENERATING

def caesar(text, shift):
    alphabet = string.ascii_uppercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return text.translate(table)

def frequency(text):

    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    freq = list()
    
    for i in range(26):
        freq.append(text.count(alpha[i]))

    return freq

if __name__ == "__main__":
    main()
