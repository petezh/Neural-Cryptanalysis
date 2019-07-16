# this code will:
# use a cipher on each sentence
# perform frequency analysis
# store (ciphertext, key) pairs

import re
import csv
import random
import string
import multiprocessing
import itertools
import numpy as np
from math import ceil

def main():
    fileName = "snippets.txt"
    process(fileName)

# calls ciphers, writes to output
def process(fileName):

    snippets = open(fileName, 'r')

    caewtr = csv.writer(open('caepairs.csv','w'))
    caewtr.writerow(['shift'] + [char for char in string.ascii_uppercase])


    affwtr = csv.writer(open('affpairs.csv','w'))
    affwtr.writerow(['shift','mult']+[char for char in string.ascii_uppercase])


    vigwtr = csv.writer(open('vigpairs.csv','w'))
    vigwtr.writerow(['key'] + [char for char in string.ascii_uppercase])
    
    hillwtr = csv.writer(open('hillpairs2x2.csv','w'))
    hillwtr.writerow(['0,0','0,1','1,0','1,1'] + [char for char in string.ascii_uppercase])
    
    for snip in snippets:

        snip = re.sub("[^a-zA-Z]+", '', snip)
        
        
        # make caesar pairs
        shift = random.randint(1, 26)
        ciphertext = caesar(snip, shift)
        freq = frequency(ciphertext)
        caewtr.writerow([shift] + freq)
        
        # make affine pairs
        shift = random.randint(1, 26)
        mults = [1,3,5,7,9,11,15,17,19,21,23,25]
        mult = random.randint(0, 11)
        ciphertext = affine(snip, mults[mult], shift)
        freq = frequency(ciphertext)

        affwtr.writerow([shift,mult] + freq)
        
        # make vegenere cipher
        length = random.randint(1, 11)
        key = list()
        for i in range(length):
            key.append(random.randint(0, 26))
        ciphertext = vigenere(snip, key)
        freq = frequency(ciphertext)
        vigwtr.writerow([key] +freq)
        
        #make hill cipher 2x2
        ciphertext = hill(snip,2)
        freq = frequency(ciphertext[0])
        key = ciphertext[1]
        hillwtr.writerow(key.flatten().tolist() + freq)


# perform a caesar cipher
def caesar(text, shift):
    alphabet = string.ascii_uppercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return text.translate(table)


# perform an affine cipher
def affine(text, mult, shift):
    alphabet = string.ascii_uppercase
    ciphertext = ""
    for char in text:
        index = ((mult * alphabet.index(char))+shift)%26
        ciphertext = ciphertext+alphabet[index]
        
    return ciphertext
    

# peform a classic vigenere cipher
def vigenere(text, key):

    alphabet = string.ascii_uppercase
    ciphertext = ""
    for i in range(len(text)):
        index = (alphabet.index(text[i]) + key[i % len(key)])%26
        ciphertext = ciphertext + alphabet[index]
        
    return ciphertext

#generate keys for hill cipher
def gen_key(dimension):
    inv = False
    while not inv:
        key = np.random.randint(size=(dimension, dimension), low=0, high=25)
        try:
            i = np.linalg.inv(key)
            inv = True
        except:
            inv = False
    return key

#performs a classic hill cipher
def hill(plaintext, dimension, key=None):
    plaintext = plaintext.upper()
    if key == None or key.shape != (dimension, dimension):
        key = gen_key(dimension)
        idx = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    while len(plaintext) % dimension != 0:
        plaintext += 'A'
    plain_arr = np.array([idx.index(let) for let in plaintext])
    plain_arr = np.reshape(plain_arr, (ceil(len(plaintext)/dimension), dimension))
    ciph_arr = []
    for sub in plain_arr:
        ciph_arr.append(np.remainder(np.matmul(sub, key),26))
    ciphertext = ''
    for sub in ciph_arr:
        for let in sub:
            ciphertext += idx[let]
    return ciphertext,key
# perform frequency analysis
def frequency(text):

    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    freq = list()
    
    for i in range(26):
        freq.append(text.count(alpha[i]))

    return freq

if __name__ == '__main__':
    main()
