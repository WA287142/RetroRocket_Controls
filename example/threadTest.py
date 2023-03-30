# Purpose of this program is to test the functionality of threading in  Python for multiple motors
import sys
import socket
import time
import threading
import queue

# sys.path.insert(8, r'C:\Users\Public\Downloads\NanoLib_1.0.1\NanoLib_Python_Windows\nanotec_nanolib_win-1.0.1\nanotec_nanolib')

# from twoMotors import move_motor, connect_motor
from nanotec_nanolib import Nanolib
from nanolib_helper import NanolibHelper
from nanolib_profinet_example import ProfinetExample
from nanolib_sampler_example import SamplerExample


def move_motor1(input):
    while True:
        data = input.get()
        if data == -1:
            
            break

        
        print('Moving motor1 to angle: ', data)

def move_motor2(input):
    while True:
        data = input.get()
        if data == -1:
            
            break
        
        print('Moving motor2 to angle: ', data)

# create a queue and a thread to run the worker function
angle1 = queue.Queue()
angle2 = queue.Queue()
# The args data type must be a tuple or else it'll give an error, so (q,) creates a single value tuple
t1 = threading.Thread(target=move_motor1, args=(angle1,))
t2 = threading.Thread(target=move_motor2, args=(angle2,))

# start the thread
t1.start()
t2.start()

# send messages to the thread
# while angle1 != -1 or angle2 != -1:
#     angle1.put(int(input('Enter angle: ')))
#     angle2.put(int(input('Enter angle: ')))


# wait for the thread to finish
t1.join()
t2.join()

print("Code Finished")