import serial
import threading
import time
import csv
import datetime

# NOTES
# ABCDE String could be changed
# Threading could be changed

# getting serial from board
espData = serial.Serial('COM3', 115200)  # COM port & BAUD rate

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

# uncomment for csv file writing
with open('5.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['time', 'thumb', 'index', 'middle', 'ring', 'pinky'])

    start_time = datetime.datetime.now()

    # Counter for number of rows written to the CSV file
    row_count = 0

    # main thread, displays data grabbed by esp thread every 1 second
    while True:
        time.sleep(0.005)
        try:
            timestamp = (datetime.datetime.now() - start_time).total_seconds()
            writer.writerow([timestamp, thumb, index, middle, ring, pinky])
            row_count += 1
            print("Output: ", output)
            print("Thumb:", thumb)
            print("Index:", index)
            print("Middle:", middle)
            print("Ring:", ring)
            print("Pinky:", pinky, "\n")

            # Check if the row count has reached the limit, and end the program if so
            if row_count >= 1500:
                break

        except:
            break
