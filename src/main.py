import sys
import tkinter as tk
import serial
import threading
import time
import tensorflow as tf
import numpy as np
from serial import SerialException

# LOAD AI MODEL
model = tf.keras.models.load_model('mind_flayer.h5')

#Set-up gui
window = tk.Tk()
window.title("AIVRGlove")
window.geometry('275x220')
window.resizable(False, False)

frame_input = tk.LabelFrame(window, text="Input")
frame_input.pack(side=tk.TOP, padx=10, pady=10)

# create labels to display the sensor data
thumb_label = tk.Label(frame_input, text="Thumb: ")
index_label = tk.Label(frame_input, text="Index: ")
middle_label = tk.Label(frame_input, text="Middle: ")
ring_label = tk.Label(frame_input, text="Ring: ")
pinky_label = tk.Label(frame_input, text="Pinky: ")

thumb_label.grid(row=0, column=0, sticky="W")
index_label.grid(row=1, column=0, sticky="W")
middle_label.grid(row=2, column=0, sticky="W")
ring_label.grid(row=3, column=0, sticky="W")
pinky_label.grid(row=4, column=0, sticky="W")

# create output frame to display data
frame_output = tk.LabelFrame(window, text="Output")
frame_output.pack(side=tk.TOP, padx=10, pady=10)

output_label = tk.Label(frame_output, text="")
output_label.pack()

espFlag = True

# provide com port and baud rate
comPort = 'COM3'
baud = 115200

# check if esp exists
try:
    espData = serial.Serial(comPort, baud)  # COM port & BAUD rate
except (SerialException):
    espFlag = False

output = ""
thumb = 0
index = 0
middle = 0
ring = 0
pinky = 0

# Function to get esp input from espInputThread (ensures timing alignment)
def espInput():
    global thumb, index, middle, ring, pinky, output

    # only reads if the board exists, will exit if board not found
    while True:
        if espFlag:
            try:
                output = espData.readline().decode('utf-8').rstrip()
                output = output.split(",")
                thumb = float(output[0]) / 1300.0
                index = float(output[1]) / 1458.0
                middle = float(output[2]) / 1798.0
                ring = float(output[3]) / 2971.0
                pinky = float(output[4]) / 1191.0

            except (UnicodeDecodeError, ValueError, IndexError):
                pass
        else:
            break

# thread that continuously runs espInput function to get data, dameon = True so that it will end with the main thread
espInputThread = threading.Thread(target=espInput)
espInputThread.daemon = True
espInputThread.start()

# labels of gestures corresponding to indexes in model
gesture_labels = ['A','B','C','D','E','F','G','H','I','K','L','O','S','W','X','Y']

# main thread, displays data grabbed by esp thread every 1 second
def updateGui():

    if not espFlag:
        output_label.config(text="Device not recognized")
    else:
        # update the label text with the latest sensor data
        thumb_label.config(text=f"Thumb: {thumb}")
        index_label.config(text=f"Index: {index}")
        middle_label.config(text=f"Middle: {middle}")
        ring_label.config(text=f"Ring: {ring}")
        pinky_label.config(text=f"Pinky: {pinky}")

        # prepare the sensor data for input to the model
        input_data = np.array([thumb, index, middle, ring, pinky]).reshape(-1, 1, 5)

        # use the model to predict the gesture
        prediction = model.predict(input_data)

        # if there is a gesture predicted above 70% accuracy, display gesture. Otherwise, invalid
        if prediction.max() > 0.7: #0.7 best?
            gesture_index = np.argmax(prediction)
            gesture = gesture_labels[gesture_index]
            output_label.config(text=f"Current Gesture: ASL {gesture}")
        else:
            output_label.config(text="Current Gesture: None")

        # update gui after 1 second
        window.after(1000, updateGui)

# update gui after 1 second
window.after(1000, updateGui)

# loop gui
window.mainloop()