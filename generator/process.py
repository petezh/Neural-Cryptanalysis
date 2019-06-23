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
    
    output = csv.writer(open('pairs.csv','w'))
    
    for snip in snippets:
        
        shift = random.randint(1, 27)
        ciphertext = caesar(snip, shift)
        freq = frequency(ciphertext)
        output.writerow([shift, freq])

# perform a caesar cipher
def caesar(snip, shift):
    alphabet = string.ascii_uppercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return snip.translate(table)

# perform frequency analysis
def frequency(text):

    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    freq = list()

    for i in range(26):
        freq.append(text.count(alpha[i]))

    return freq

if __name__ == '__main__':
    main()
