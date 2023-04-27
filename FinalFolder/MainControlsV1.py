# In V1 of MainControls.py, a server is hosted to take in data from the VR sim
# Purpose of this program is to connect to and control six Nanotec motors simultaneously
# To install numpy and scipy in the right directory, needed to run 'py -3.10 -m pip install scipy'

# TO RUN THIS CODE
# Once you run this file, you need to connect to the server/port with either dataSender.py or a UE5 client
# You send in a value which is the angle you want the motor to go to
import pickle
import sys
import socket
import time
import numpy as np

import KuskodeV2 as kine
import motorFunctions as MF
from nanotec_nanolib import Nanolib
from nanolib_helper import NanolibHelper
from nanolib_profinet_example import ProfinetExample
from nanolib_sampler_example import SamplerExample

# Setup motor controls
nanolib_helper = NanolibHelper()

# create access to the nanolib
nanolib_helper.setup()


# Use Connect_motor() to connect to both motors
# the id is equivalent to the index that the device will show up as in example.py
# the id is 0 for both because after connecting to one device, the device no longer shows and index shifts left
motor4 = MF.connect_motor(nanolib_helper, 0)
motor3 = MF.connect_motor(nanolib_helper, 0)
motor2 = MF.connect_motor(nanolib_helper, 0)
motor6 = MF.connect_motor(nanolib_helper, 0)
motor5 = MF.connect_motor(nanolib_helper, 0)
motor1 = MF.connect_motor(nanolib_helper, 0)

# Set the max motor speed
MF.setMaxSpeed(nanolib_helper, motor1, 500)
MF.setMaxSpeed(nanolib_helper, motor2, 500)
MF.setMaxSpeed(nanolib_helper, motor3, 500)
MF.setMaxSpeed(nanolib_helper, motor4, 500)
MF.setMaxSpeed(nanolib_helper, motor5, 500)
MF.setMaxSpeed(nanolib_helper, motor6, 500)

# Set acceleration
MF.setAcceleration(nanolib_helper, motor1, 1000)
MF.setAcceleration(nanolib_helper, motor2, 1000)
MF.setAcceleration(nanolib_helper, motor3, 1000)
MF.setAcceleration(nanolib_helper, motor4, 1000)
MF.setAcceleration(nanolib_helper, motor5, 1000)
MF.setAcceleration(nanolib_helper, motor6, 1000)

# Move the motor to position 0 before beginning
# May remove for actual demonstration
# MF.move_motor(nanolib_helper, motor1, 0, 'abs')
# MF.move_motor(nanolib_helper, motor2, 0, 'abs')
# MF.move_motor(nanolib_helper, motor3, 0, 'abs')
# MF.move_motor(nanolib_helper, motor4, 0, 'abs')
# MF.move_motor(nanolib_helper, motor5, 0, 'abs')
# MF.move_motor(nanolib_helper, motor6, 0, 'abs')

# time.sleep(3)

MF.move_motor(nanolib_helper, motor1, 0, 'abs')
MF.move_motor(nanolib_helper, motor2, 0, 'abs')
MF.move_motor(nanolib_helper, motor3, 0, 'abs')
MF.move_motor(nanolib_helper, motor4, 0, 'abs')
MF.move_motor(nanolib_helper, motor5, 0, 'abs')
MF.move_motor(nanolib_helper, motor6, 0, 'abs')


time.sleep(2) 


# Create the server to connect to. Need to move the main code into the nested while loop when ready
try:
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

    # conn.sendall("Data received to Server".encode())

    from_client = ''
    f = open("flightTestOutput.txt", 'w')

    while True:
        # time.sleep(1)
        # By sending this message, we tell the VR side that the data has been processed and motors have been moved and can now take in a new data point.
        conn.sendall('Server received message'.encode())
        data = conn.recv(4096)
        # if not data:
        #     # disconnect the motor
        #     nanolib_helper.disconnect_device(motor1)
        #     nanolib_helper.disconnect_device(motor2)
        #     nanolib_helper.disconnect_device(motor3)
        #     nanolib_helper.disconnect_device(motor4)
        #     nanolib_helper.disconnect_device(motor5)
        #     nanolib_helper.disconnect_device(motor6)

        #     # close the server connection
        #     conn.close()
        #     print("\nClosed everything successfully\n")
        #     sys.exit()
        data = data.decode()
        # print("Client says: "+ data)
        # Take in data and convert to floats and send to Kuskode
        # data = pickle.loads(data)
        # print("DATA = ", data)
        # Data is taken in as a string but contains P=1234.0 Y=1234.0 R=1234.0 . Need to Remove the Letters and ='s
        # Split('=') should result in P, 1234.0 Y, 1234.0 R, 1234.0
        data = data.split('P')
        lastpt = data[-1]
        lastpt = lastpt.split('=')
        # print("lastpt:", lastpt)
        


        # print("DATA = ", data)
        # Taking the 2nd index, [1], we store everything but the last two indices into variable pitch
        pitchData = lastpt[1]
        yawData = lastpt[2]
        roll = float(lastpt[3])/6
        pitch = float(pitchData[:-2])/3
        # for yaw, we take the 3rd index [2] and store everything but the last 2 indicies of the index into variable yaw
        
        yaw = float(yawData[:-2])/6
        # roll is only numbers so we can store it directly into vairable roll
        
        # These are for debugging
        # print('yaw', yaw)
        # print('pitch', pitch)
        # print('roll', roll)

        # Input Kuskode here
        # First 3 parameters are x,y,z translation. Not needed currently so set to 0. z is set to 25.5 since the platform is set 25.5 in off the ground
        # 4th parameter is yaw. We don't consider yaw so set it to 0 for now.
        angles = kine.get_inv_kine(0, 0, 25.5, 0, pitch, roll, False, True, True)
        print('angles = ', angles)
        gear_ratio = 10
        f.write(str(angles) + "\n")
        if(angles[0] != -99999):
            
            MF.move_motor(nanolib_helper, motor1, int(angles[0])*gear_ratio, 'abs')
            MF.move_motor(nanolib_helper, motor2, int(angles[1])*gear_ratio, 'abs')
            MF.move_motor(nanolib_helper, motor3, int(angles[2])*gear_ratio, 'abs')
            MF.move_motor(nanolib_helper, motor4, int(angles[3])*gear_ratio, 'abs')
            MF.move_motor(nanolib_helper, motor5, int(angles[4])*gear_ratio, 'abs')
            MF.move_motor(nanolib_helper, motor6, int(angles[5])*gear_ratio, 'abs')
        


    # conn.close()
    # print('client disconnected')

    # break

# # Disconnect the motor
# nanolib_helper.disconnect_device(motor1)
# nanolib_helper.disconnect_device(motor2)

# # bus_hw_id isnt accessible bc it is inside the scope of the connect_motor() function
# # nanolib_helper.close_bus_hardware(bus_hw_id)

# print("Closing everything successfully")