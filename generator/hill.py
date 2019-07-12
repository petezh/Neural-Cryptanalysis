import numpy as np
from math import ceil

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


def encrypt(plaintext, dimension, key=None):
    plaintext = plaintext.upper()
    if key == None or a.shape != (dimension, dimension):
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
    return plaintext, ciphertext

print(encrypt('TEST', 2))


