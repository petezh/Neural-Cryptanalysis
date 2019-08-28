# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 14:19:22 2019

@author: patri
"""
import pycipher as ci
from random import randint

file = 'snippets_len500.txt'
f = open(file,'r')
li = []
def genRandomKey():
    x = randint(5,20) #5 <= x <= 20
    alpha = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    key = ''
    for i in range(x):
        key += alpha[randint(0,25)]
    return key
for snip in f:
    key = genRandomKey()
    encrypt = ci.Vigenere(key).encipher(snip)
    li.append([key,encrypt])
print('done')