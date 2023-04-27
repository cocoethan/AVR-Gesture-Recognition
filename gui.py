import sys
import tkinter as tk
import serial
import threading
import time

from serial import SerialException

#Set-up Window
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

frame_output = tk.LabelFrame(window, text="Output")
frame_output.pack(side=tk.TOP, padx=10, pady=10)

output_label = tk.Label(frame_output, text="Current Gesture: None")
output_label.pack()

# get serial from board

try:
    espData = serial.Serial('COM3', 115200)  # COM port & BAUD rate
except (SerialException):
    print("Device not recognized")
    sys.exit()

output = ""
thumb = 0
index = 0
middle = 0
ring = 0
pinky = 0

# ESP returning ABCDE string. Need to change later, but can parse with this for now. FNCTN is getting data constantly in its own thread
def espInput():
    global thumb, index, middle, ring, pinky, output

    while True:
        try:
            output = espData.readline().decode('utf-8').rstrip()
            output = output.split(",")
            thumb = int(output[0])
            index = int(output[1])
            middle = int(output[2])
            ring = int(output[3])
            pinky = int(output[4])

        except (UnicodeDecodeError, ValueError, IndexError):
            pass

# thread that continuously runs espInput function to get data
espInputThread = threading.Thread(target=espInput)
espInputThread.daemon = True
espInputThread.start()

# main thread, displays data grabbed by esp thread every 1 second
def updateGui():
    # update the label text with the latest sensor data
    thumb_label.config(text=f"Thumb: {thumb}")
    index_label.config(text=f"Index: {index}")
    middle_label.config(text=f"Middle: {middle}")
    ring_label.config(text=f"Ring: {ring}")
    pinky_label.config(text=f"Pinky: {pinky}")

    #can do model predict stuff here
    #model.predict()

    # if predict predicts letter, display letter, if no letter, display "None"
    # set output = to that

    output = "None"

    output_label.config(text=f"Current Gesture: {output}")
    # schedule the next update
    window.after(1000, updateGui)

# schedule the first update
window.after(1000, updateGui)

window.mainloop()
