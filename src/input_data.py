import serial
import threading
import time
import csv
import datetime

# getting serial from board
espData = serial.Serial('COM3', 115200)  # COM port & BAUD rate

output = ""
thumb = 0
index = 0
middle = 0
ring = 0
pinky = 0

# Function to get esp input from espInputThread (ensures timing alignment)
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

# for csv file writing, will end when 1500 data points are collected
# make csv file name user number.
with open('1.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['time', 'thumb', 'index', 'middle', 'ring', 'pinky'])

    start = datetime.datetime.now()

    # Counter for number of rows written to the CSV file
    rows = 0

    # main thread, displays data grabbed by esp, writes to csv file
    while True:
        time.sleep(0.005)
        try:
            # display for data validation
            print("Output: ", output)
            print("Thumb:", thumb)
            print("Index:", index)
            print("Middle:", middle)
            print("Ring:", ring)
            print("Pinky:", pinky, "\n")

            # timestamps for model training
            timestamp = (datetime.datetime.now() - start).total_seconds()
            # prints as simple csvals
            writer.writerow([timestamp, thumb, index, middle, ring, pinky])
            rows += 1

            # Check if the row count has reached the limit, and end the program if so
            if rows >= 1500:
                break

        except:
            break