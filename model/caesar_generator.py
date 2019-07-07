import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #some visuals, dont need in program

def train(length, lang):
    yield "Setting up model..."
    dataPath = 'caepairs.csv'
    data = pd.read_csv(dataPath).values
    labels = []
    datas = []
    for i in range(0, len(data)):
        labels.append((data[i][0]-1)%26)
        datas.append(data[i][1:])
    for i in range(0, len(data)):
        datas[i] = np.true_divide(datas[i], np.sum(datas[i]))
    model = keras.Sequential()
    model.add(keras.layers.Dense(26, activation = tf.nn.sigmoid))
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    trial_data = datas[:1500]
    test_data = datas[1500:]
    trial_labels = labels[:1500]
    test_labels = labels[1500:]
    yield "Training model..."
    model.fit(np.array(trial_data), np.array(trial_labels), epochs=100, batch_size = 32)
    yield "Training complete. Testing model..."
    results = model.evaluate(np.array(test_data), np.array(test_labels))
    yield "Testing complete. Accuracy: %f" % results[1]
