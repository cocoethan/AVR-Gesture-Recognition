import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import random

import tensorflow
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

dataset_dir = 'C:/Users/ethan/Desktop/ASLDataset/training_data/' #Dataset local directory
testing_dataset_dir = 'C:/Users/ethan/Desktop/ASLDataset/testing_data/' #Testing Dataset local directory
categories = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'] #List of data categories
#categories = ['a','b','c']

training_data = []
testing_data = []

feature_set = [] #x-train
label_set = [] #y-train

feature_test_set = [] #x-test
label_test_set = [] #y-test

for category in categories:
    path = os.path.join(dataset_dir, category) #Path to categories
    category_num = categories.index(category)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        data = pd.read_csv(file_path)
        data = data.values
        training_data.append([data[:, 2:22], category_num])

for category in categories:
    path = os.path.join(testing_dataset_dir, category)  # Path to categories
    category_num = categories.index(category)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        data = pd.read_csv(file_path)
        data = data.values
        testing_data.append([data[:, 2:22], category_num])

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

feature_set = np.array(feature_set).reshape(-1, 1500, 20)
#label_set = np.array(label_set)
#print(label_set.shape)
label_set = np.array(label_set).reshape(-1,)

#use pickle here

model = Sequential()
model.add(keras.Input(shape=(1500, 20)))
model.add(keras.layers.SimpleRNN(128, return_sequences=True, activation='relu'))
model.add(keras.layers.SimpleRNN(128, return_sequences=False, activation='relu'))
model.add(keras.layers.Dense(26))

loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optim = keras.optimizers.Adam(learning_rate=0.001)
metrics = ["accuracy"]

model.compile(loss=loss, optimizer=optim, metrics=metrics)

batch_size = 64
epochs = 20

model.fit(feature_set, label_set, batch_size = batch_size, epochs = epochs)

#model.evaluate()

######################
#model = Sequential()
#model.add(LSTM(128, input_shape=(1500, 5), return_sequences=True)) ##
#model.add(Dropout(0.2))
#model.add(LSTM(128))
#model.add(Dropout(0.2))
#model.add(Dense(32, activation='relu'))
#model.add(Dropout(0.2))
#model.add(Dense(26, activation='softmax')) #3 is hardcoded #change

##opt = tf.keras.optimizers.legacy.Adam(learning_rate=1e-1, decay=1e-3) #decay=1e-5

#model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#model.summary()

#model.fit(feature_set, label_set, epochs=3) #add tests

test_loss, test_acc = model.evaluate(feature_set, label_set)
print("\nSet Accuracy:", test_acc)

test_loss, test_acc = model.evaluate(feature_test_set, label_test_set)

print("\nTest Accuracy:", test_acc)

###############
