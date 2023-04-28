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
#categories = ['a','b','c']
categories = ['a','b','c','d','e','f','g','h','i','k','l','o','s','w','x','y']

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

        #data[:, 2:7][data[:, 2:7] < 0] = 0
        #data[:, 2:7][data[:, 2:7] > 100] = 100
        #data[:, 2:7] = data[:, 2:7] / 100

        #training_data.append([data[:, 2:7], category_num])
        training_data.append([data[:, 1:6], category_num])

#print(training_data)

for category in categories:
    path = os.path.join(testing_dataset_dir, category)  # Path to categories
    category_num = categories.index(category)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        data = pd.read_csv(file_path)
        data = data.values

        #data[:, 2:7][data[:, 2:7] < 0] = 0
        #data[:, 2:7][data[:, 2:7] > 100] = 100
        #data[:, 2:7] = data[:, 2:7] / 100

        testing_data.append([data[:, 1:6], category_num]) #2:22

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

print(feature_set.shape)
print(feature_test_set.shape)

feature_set = np.array(feature_set).reshape(-1, 1500, 5) #(-1, 1500, 20)
label_set = np.array(label_set).reshape(-1,)

feature_test_set = np.array(feature_test_set).reshape(-1, 450, 5)
label_test_set = np.array(label_test_set).reshape(-1,)

#feature_set = to_categorical(feature_set, 24)
label_set = to_categorical(label_set, 16)
#label_set = to_categorical(label_set, 26)
#feature_test_set = to_categorical(feature_set, 24)
label_test_set = to_categorical(label_test_set, 16)
#label_test_set = to_categorical(label_test_set, 26)

#use pickle here

model = Sequential()
model.add(keras.layers.GRU(units=64, return_sequences=True, input_shape=(1500, 5), kernel_regularizer=regularizers.l2(0.01))) #activation='tanh' units=64, return_sequences=True, input_shape=(1500, 5), kernel_regularizer=regularizers.l2(0.01)
model.add(keras.layers.GRU(units=64, return_sequences=False, input_shape=(1500, 5), kernel_regularizer=regularizers.l2(0.01)))
model.add(keras.layers.Dense(units=32))
##model.add(keras.layers.Dense(units=16, activation='softmax'))
model.add(keras.layers.Dense(units=16, activation='softmax'))
#model.add(BatchNormalization())
##model.add(keras.Input(shape=(1500, 5))) #(-1, 1500, 20)
#model.add(BatchNormalization()) #
##model.add(keras.layers.SimpleRNN(64, return_sequences=True, activation='relu', kernel_regularizer=regularizers.l2(0.01))) #128#relu #kernel_regularizer=regularizers.l2(0.01) #SimpleRNN
#model.add(keras.layers.Dropout(0.1))
##model.add(keras.layers.SimpleRNN(64, return_sequences=False, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
#model.add(keras.layers.Dropout(0.1))
#model.add(keras.layers.Dense(36))
#model.add(keras.layers.Dense(24))
##model.add(keras.layers.Dense(16))
#model.add(keras.layers.Dense(26, activation='softmax'))

#loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True) #from_logits=True
#optim = keras.optimizers.Adam(learning_rate=0.001) #learning_rate=0.001
#metrics = ["accuracy"]
model.summary()

optim = keras.optimizers.Adam(clipnorm=1.0)

#model.compile(loss=loss, optimizer=optim, metrics=metrics)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#batch_size = 25 #64
epochs = 120

#history = model.fit(feature_set, label_set, batch_size = batch_size, epochs = epochs)
history = model.fit(feature_set, label_set, epochs = epochs)
pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
#save_fig("keras_learning_curves_plot")
plt.show()


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

model.save('mind_flayer.h5')

###############


