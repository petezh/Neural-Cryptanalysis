from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds


train_file_path = tf.keras.utils.get_file("caepairs.csv", "https://github.com/petezh/UMD-2019/blob/master/generator/caepairs.csv")

np.set_printoptions(precision=3, suppress=True)

with open(train_file_path, 'r') as f:
    names_row = f.readline()


CSV_COLUMNS = names_row.rstrip('\n').split(',')
print(CSV_COLUMNS)

