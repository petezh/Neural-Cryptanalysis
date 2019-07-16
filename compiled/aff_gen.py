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


# AFFINE


def affine_encrypt(length, lang):
    snippets = open(lang + "snip" + str(length) + '.txt', 'r')
    affFile = open('affpairs.csv','w')
    affwtr = csv.writer(affFile)
    affwtr.writerow(['shift','mult']+[char for char in string.ascii_uppercase])

    for snip in snippets:

        snip = re.sub("[^a-zA-Z]+", '', snip)
        
        
        # make affine pairs
        shift = random.randint(1, 26)
        mults = [1,3,5,7,9,11,15,17,19,21,23,25]
        mult = random.randint(0, 11)
        ciphertext = affine(snip, mults[mult], shift)
        freq = frequency(ciphertext)

        affwtr.writerow([shift, mult] + freq)
        
    affFile.close()
    print("Generated affine ciphertexts.")

def affine(text, mult, shift):
    alphabet = string.ascii_uppercase
    ciphertext = ""
    for char in text:
        index = ((mult * alphabet.index(char))+shift)%26
        ciphertext = ciphertext+alphabet[index]
        
    return ciphertext


def frequency(text):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    freq = list()
    for i in range(26):
        freq.append(text.count(alpha[i]))
    return freq

if __name__ == "__main__":
    main()
