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

def main():
    vig_encrypt()


def vig_encrypt():
    
    snippets = open('snippets_len250.txt', 'r')
    vigFile = open('vigpairs.csv','w')
    vigwtr = csv.writer(vigFile)
    vigwtr.writerow(['len']+[char for char in string.ascii_uppercase])

    for snip in snippets:

        snip = re.sub("[^a-zA-Z]+", '', snip)
        
        
        # make affine pairs
        leng = random.randint(3, 5)
        key = ""
        for i in range(0, leng):
            key += random.choice(string.ascii_letters)
        ciphertext = vigenere(snip, key.upper())
        freq = frequency(ciphertext)

        vigwtr.writerow([leng] + freq)
        
    vigFile.close()
    print("Generated vigenere ciphertexts.")
    return "Generated vigenere ciphertexts."


# peform a classic vigenere cipher
def vigenere(text, key):

    print(key)
    alphabet = string.ascii_uppercase
    ciphertext = ""
    for i in range(len(text)):
        index = (alphabet.index(text[i]) + alphabet.index(key[i % len(key)]))%26
        ciphertext = ciphertext + alphabet[index]
        
    return ciphertext




def frequency(text):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    freq = list()
    for i in range(26):
        freq.append(text.count(alpha[i]))
    return freq

if __name__ == "__main__":
    main()
