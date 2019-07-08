# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 11:34:26 2019

@author: patri
"""
import math
from collections import Counter
import pandas as pd
import numpy as np


#english
letterfreq ={'E' : 12.0, 'T' : 9.10, 'A' : 8.12, 'O' : 7.68, 'I' : 7.31, 'N' : 6.95, 'S' : 6.28, 'R' : 6.02, 'H' : 5.92, 'D' : 4.32, 'L' : 3.98, 'U' : 2.88, 'C' : 2.71, 'M' : 2.61, 'F' : 2.30, 'Y' : 2.11, 'W' : 2.09, 'G' : 2.03, 'P' : 1.82, 'B' : 1.49, 'V' : 1.11, 'K' : 0.69,'X' : 0.17, 'Q' : 0.11, 'J' : 0.10, 'Z' : 0.07 }

#spanish
#letterfreq ={'E' : 13.72, 'A' : 11.72, 'O' : 8.44, 'S' : 7.2, 'N' : 6.83, 'R' : 6.41, 'I' : 5.28, 'L' : 5.24, 'D' : 4.67, 'T' : 4.6, 'U' : 4.55, 'C' : 3.87, 'M' : 3.08, 'P' : 2.89, 'B' : 1.49, 'H' : 1.18, 'Q' : 1.11, 'Y' : 1.09, 'V' : 1.05, 'G' : 1, 'F' : 0.69, 'J' : 0.52, 'Z' : 0.47, 'X' : 0.14, 'K' : 0.11, 'W' : 0.04}

let = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
frequencies = []
for x in let:
    frequencies.append(round(letterfreq[x]/100,4))
#takes a list of frequencies, returns the shift number that maximizes the dot product
def test(data):
    dot = []
    for x in range(0,26):
        shift = data.tolist()[x:] + data.tolist()[:x]
        dot.append(np.dot(np.array(frequencies),np.array(shift)))
    return dot.index(max(dot))

data = pd.read_csv("caepairs.csv").values
labels = []
datas = []
#formatting
for i in range(0,len(data)):
    labels.append((data[i][0])%26)
    datas.append(data[i][1:])

#normalize to [0,1] frequencies

for i in range(0,len(data)):
    datas[i] = np.true_divide(datas[i], np.sum(datas[i]))
x = [test(y) for y in datas]
count = [(y == z) for y,z in zip(x,labels)]
count = sum(count)
print(count/len(data))
        
