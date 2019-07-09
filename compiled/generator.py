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

def main():
    generate(2, "span")

def generate(length, lang):
    
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

def caesar_encrypt(length, lang):
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
