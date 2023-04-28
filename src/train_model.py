import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import random

import tensorflow as tf
from keras import regularizers
from keras.layers import BatchNormalization
from keras.utils import to_categorical
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

dataset_dir = 'C:/Users/ethan/Desktop/AVRDataset/asl/training_set_normalized/' #Dataset local directory
testing_dataset_dir = 'C:/Users/ethan/Desktop/AVRDataset/asl/testing_set_normalized/' #Testing Dataset local directory
#categories = ['a','b','c','d','e','f','g','h','i','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y'] #List of data categories #j and z out
categories = ['a','b','c','d','e','f','g','h','i','k','l','o','s','w','x','y']

training_data = []
testing_data = []

feature_set = [] #x-train
label_set = [] #y-train

feature_test_set = [] #x-test
label_test_set = [] #y-test

categories_len = len(categories);

for category in categories:
    path = os.path.join(dataset_dir, category) #Path to categories
    category_num = categories.index(category)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        data = pd.read_csv(file_path)
        data = data.values[:, 1:6]
        for i in range(len(data)):
            line_data = data[i]
            training_data.append([line_data, category_num])

for category in categories:
    path = os.path.join(testing_dataset_dir, category)  # Path to categories
    category_num = categories.index(category)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        data = pd.read_csv(file_path)
        data = data.values[:, 1:6]
        for i in range(len(data)):
            line_data = data[i]
            testing_data.append([line_data, category_num])

random.shuffle(training_data)
random.shuffle(testing_data)

for features, label in training_data:
    feature_set.append(features)
    label_set.append(label)

for features, label in testing_data:
    feature_test_set.append(features)
    label_test_set.append(label)

feature_set = np.array(feature_set)
label_set = np.array(label_set)

feature_test_set = np.array(feature_test_set)
label_test_set = np.array(label_test_set)

feature_set = np.array(feature_set).reshape(-1, 1, 5)
label_set = np.array(label_set).reshape(-1,)

feature_test_set = np.array(feature_test_set).reshape(-1, 1, 5)
label_test_set = np.array(label_test_set).reshape(-1,)

label_set = to_categorical(label_set, categories_len)
label_test_set = to_categorical(label_test_set, categories_len)

model = Sequential()
model.add(keras.layers.GRU(units=32, input_shape=(1, 5), kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.5))
model.add(keras.layers.Dense(units=categories_len, activation='softmax'))

model.summary()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

epochs = 20

history = model.fit(feature_set, label_set, epochs = epochs)
pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.show()

test_loss, test_acc = model.evaluate(feature_set, label_set)
print("\nSet Accuracy:", test_acc)

test_loss, test_acc = model.evaluate(feature_test_set, label_test_set)

print("\nTest Accuracy:", test_acc)

#uncomment to save model
#model.save('mind_flayer.h5')
