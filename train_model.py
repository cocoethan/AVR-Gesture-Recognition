import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import random
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM


dataset_dir = 'C:/Users/ethan/Desktop/ASLData/' #Dataset local directory
categories = ["a", "b", "c"] #List of data categories

training_data = []

feature_set = []
label_set = []

for category in categories:
    path = os.path.join(dataset_dir, category) #Path to categories
    category_num = categories.index(category)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        data = pd.read_csv(file_path)
        data = data.values
        training_data.append([data[:, 2:7], category_num])

random.shuffle(training_data)

for features, label in training_data:
    feature_set.append(features)
    label_set.append(label)

feature_set = np.array(feature_set).reshape(-1, 1500, 5)
label_set = np.array(label_set)

#use pickle here

model = Sequential()
model.add(LSTM(128, input_shape=(1500, 5), return_sequences=True)) ##
model.add(Dropout(0.2))
model.add(LSTM(128))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(3, activation='softmax')) #3 is hardcoded

opt = tf.keras.optimizers.legacy.Adam(learning_rate=1e-3, decay=1e-5)

model.compile(loss='sparse_categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

model.fit(feature_set, label_set, epochs=10) #add tests

test_loss, test_acc = model.evaluate(feature_set, label_set)

print("\nAccuracy:", test_acc)
