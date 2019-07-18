import numpy as np
from math import ceil


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

def main():
    fileName = "snippets.txt"
    process(fileName)

# calls ciphers, writes to output
def process(fileName):

    snippets = open(fileName, 'r')

    hillwtr = csv.writer(open('hillpairs.csv','w'), lineterminator = "\n")
    hillwtr.writerow(['key1', 'key2', 'key3', 'key4'] + [char for char in string.ascii_uppercase])

    i = 0
    for snip in snippets:
        i += 1
        print(i)
        snip = re.sub("[^a-zA-Z]+", '', snip)
        
        
        # make caesar pairs
        shift = random.randint(1, 26)
        key = gen_key(2)
        ciphertext = encrypt(snip, 2, key)
        freq = frequency(ciphertext)
        hillwtr.writerow(list(key[0]) + list(key[1]) + freq)
        



# perform frequency analysis
def frequency(text):

    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    freq = list()
    
    for i in range(26):
        freq.append(text.count(alpha[i]))

    return freq



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


def encrypt(plaintext, dimension, key):
    idx = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    plaintext = plaintext.upper()
        
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
    return ciphertext


if __name__ == '__main__':
    main()
