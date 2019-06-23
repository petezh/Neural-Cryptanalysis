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
    
    output = csv.writer(open('pairs.txt','w'))
    
    for snip in snippets:
        shift = random.randint(1, 27)
        ciphertext = caesar(snip, shift)

        output.writerow([shift, ciphertext])

# perform encryption
def caesar(snip, shift):
    alphabet = string.ascii_uppercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return snip.translate(table)
    
if __name__ == '__main__':
    main()
