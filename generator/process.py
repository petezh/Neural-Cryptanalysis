# this code will:
# use a cipher on each sentence
# perform frequency analysis
# store (ciphertext, key) pairs

import csv
import random
import string

def main():
    fileName = "snippets.txt"
    process(fileName)

# calls ciphers, writes to output
def process(fileName):

    snippets = open(fileName, 'r')

    caewtr = csv.writer(open('caepairs.csv','w'))
    affwtr = csv.writer(open('affpairs.csv','w'))
    
    for snip in snippets:

        # make caesar pairs
        shift = random.randint(1, 27)
        ciphertext = caesar(snip, shift)
        freq = frequency(ciphertext)
        caewtr.writerow([shift, freq])
        
        # make affine pairs
        shift = random.randint(1, 27)
        mult = random.choice([1,3,5,7,9,11,15,17,19,21,23,25])
        ciphertext = affine(snip, mult, shift)
        freq = frequency(ciphertext)
        affwtr.writerow([shift, mult, freq])


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
        if char.isalpha():
            index = ((mult * alphabet.index(char))+shift)%26
            ciphertext = ciphertext+alphabet[index]
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
