# Purpose of this program is to connect to and control two Nanotec motors simultaneously

import sys
import socket
import time
sys.path.insert(8, r'C:\Users\Public\Downloads\NanoLib_1.0.1\NanoLib_Python_Windows\nanotec_nanolib_win-1.0.1\nanotec_nanolib')

import motorFunctions as MF
from nanotec_nanolib import Nanolib
from nanolib_helper import NanolibHelper
from nanolib_profinet_example import ProfinetExample
from nanolib_sampler_example import SamplerExample



# This is to create the server to connect to. Need to move the main code into the nested while loop when ready
""" try:
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # AF_INET is the address-family ipv4
        # SOCK_STREAM is connection oriented TCP protocol
except socket.error as err:
    print("Server creation failed: %s" %(err))

# set the socket options to allow multiple connections
serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 7000   # Default port for socket

serv.bind(('127.0.0.1', port))
print("socket binded to %s" %(port))

serv.listen(5)  # Listen for connections made to the server. The 5 is the max number of connections
print("socket listen")

while True:
    conn, addr = serv.accept()  # accepting a connection request from client
        # addr stores the address from which the connection came from
    print('Got connection from ', addr)

    conn.sendall("Sending encoded byte type confirmation message from SERVER".encode())

    from_client = ''
    
    while True:
        data = conn.recv(4096)
        if not data:
            break
        
        print ("Client says: "+data.decode())

        conn.sendall('Server received message'.encode())


    conn.close()
    print('client disconnected')

    break """
################################################# MAIN ####################################

nanolib_helper = NanolibHelper()

# create access to the nanolib
nanolib_helper.setup()

# Use Connect_motor() to connect to both motors
# the id is equivalent to the index that the device will show up as in example.py
# the id is 0 for both because after connecting to one device, the device no longer shows and index shifts left
motor1 = MF.connect_motor(nanolib_helper, 0)
motor2 = MF.connect_motor(nanolib_helper, 0)


###########################################################################
# Allows User to input desired angle for both motors until -1 is entered
# val = int(input("Enter angle: "))

# while(val != -1):
#     move_motor(nanolib_helper, device1_handle, val)
#     move_motor(nanolib_helper, device2_handle, val)
#     val = int(input("Enter angle: "))

# ###############################################################################
# Runs through 360 degrees of motion in 1 degree increments

# Move the motor to position 0 before beginning
MF.move_motor(nanolib_helper, motor1, 0)
MF.move_motor(nanolib_helper, motor2, 0)
time.sleep(3)

for i in range(1,361):
    MF.move_motor(nanolib_helper, motor1, i)
    MF.move_motor(nanolib_helper, motor2, i)
    time.sleep(.05)


# Disconnect the motor

nanolib_helper.disconnect_device(motor1)
nanolib_helper.disconnect_device(motor2)

# bus_hw_id isnt accessible bc it is inside the scope of the connect_motor() function
# nanolib_helper.close_bus_hardware(bus_hw_id)

print("Closing everything successfully")
    


# NOTE: I set the object 6080h to 100 to fix the motor speed. It was originally set to 30000 and I don't know the units
#       Supposedly the units are user defined so I'm guessing it was 30000 deg/sec or smth.