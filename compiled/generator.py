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
    generate(2, "span")

def generate(length, lang):
    
    wordList = eval(next(open(lang + "_alltext.txt", 'r')))
    
    # define output file
    snipOut = open(lang + "snip" + str(length) + '_' + '.txt', 'w')

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

    return "Cut "+str(nosnips) + " snips."

def encrypt(length, lang, enc):

    enc_dict = {'caesar':caesar_encrypt, 'affine':affine_encrypt, 'hill':hill_encrypt}

    return enc_dict[enc](length, lang)

def caesar_encrypt(length, lang):
    snippets = open(lang + "snip" + str(length) + '.txt', 'r')
    caefile = open(lang + '_' + str(length) + '_' + 'cae.csv','w')
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
    return "Generated caesar ciphertexts."

def caesar(text, shift):
    alphabet = string.ascii_uppercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return text.translate(table)

def affine_encrypt(length, lang):
    snippets = open(lang + "snip" + str(length) + '.txt', 'r')
    affFile = open(lang + '_' + str(length) + '_' + 'aff.csv','w')
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
    return "Generated affine ciphertexts."

def affine(text, mult, shift):
    alphabet = string.ascii_uppercase
    ciphertext = ""
    for char in text:
        index = ((mult * alphabet.index(char))+shift)%26
        ciphertext = ciphertext+alphabet[index]
        
    return ciphertext

def hill_encrypt(length, lang):
    #TODO
    pass



def vig_encrypt(length, lang):
    
    snippets = open(lang + "snip" + str(length) + '.txt', 'r')
    vigFile = open(lang + '_' + str(length) + '_' + 'vig.csv','w')
    vigwtr = csv.writer(vigFile)
    vigwtr.writerow(['len']+[char for char in string.ascii_uppercase])

    for snip in snippets:

        snip = re.sub("[^a-zA-Z]+", '', snip)
        
        
        # make affine pairs
        leng = random.randint(1, 11)
        key = ""
        for i in range(0, leng):
            key += random.choice(string.ascii_letters)
        ciphertext = vigenere(snip, key)
        freq = frequency(ciphertext)

        vigwtr.writerow([leng] + freq)
        
    vigFile.close()
    print("Generated vigenere ciphertexts.")
    return "Generated vigenere ciphertexts."


# peform a classic vigenere cipher
def vigenere(text, key):

    alphabet = string.ascii_uppercase
    ciphertext = ""
    for i in range(len(text)):
        index = (alphabet.index(text[i]) + key[i % len(key)])%26
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
