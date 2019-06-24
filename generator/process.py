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

    caewtr = csv.writer(open('caepairs.csv','w'))
    affwtr = csv.writer(open('affpairs.csv','w'))
    vigwtr = csv.writer(open('vigpairs.csv','w'))
    
    for snip in snippets:

        snip = re.sub("[^a-zA-Z]+", '', snip)

        
        # make caesar pairs
        shift = random.randint(1, 27)
        ciphertext = caesar(snip, shift)
        freq = frequency(ciphertext)
        caewtr.writerow([shift, freq])
        
        # make affine pairs
        shift = random.randint(1, 27)
        mults = [1,3,5,7,9,11,15,17,19,21,23,25]
        mult = random.rantint(0, 13)
        ciphertext = affine(snip, mults[mult], shift)
        freq = frequency(ciphertext)
        affwtr.writerow([mult*26+shift, freq])

        # make vegenere cipher
        length = random.randint(1, 11)
        key = list()
        for i in range(length):
            key.append(random.randint(0, 26))
        ciphertext = vigenere(snip, key)
        freq = frequency(ciphertext)
        vigwtr.writerow([key, freq])




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

# perform frequency analysis
def frequency(text):

    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    freq = list()
    
    for i in range(26):
        freq.append(text.count(alpha[i]))

    return freq

if __name__ == '__main__':
    main()
