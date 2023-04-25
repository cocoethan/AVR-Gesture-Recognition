import serial
import threading
import time

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
            thumb = int(output[1:output.index("B")])
            index = int(output[output.index("B") + 1:output.index("C")])
            middle = int(output[output.index("C") + 1:output.index("D")])
            ring = int(output[output.index("D") + 1:output.index("E")])
            pinky = int(output[output.index("E") + 1:output.index("F")])
        except (UnicodeDecodeError, ValueError):
            pass

# thread that continuously runs espInput function to get data
espInputThread = threading.Thread(target=espInput)
espInputThread.daemon = True
espInputThread.start()

# main thread, displays data grabbed by esp thread every 1 second
while True:
    time.sleep(1)
    try:
        print("Output:", output)
        print("Thumb:", thumb)
        print("Index:", index)
        print("Middle:", middle)
        print("Ring:", ring)
        print("Pinky:", pinky, "\n")
    except:
        break