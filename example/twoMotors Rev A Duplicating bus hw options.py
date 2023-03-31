# Purpose of this program is to connect to and control two Nanotec motors simultaneously

#import sys
#import socket
import time
import numpy as np
import KuskodeV1 as kine
import motorFunctions as MF
from nanotec_nanolib import Nanolib
from nanolib_helper import NanolibHelper
from nanolib_profinet_example import ProfinetExample
from nanolib_sampler_example import SamplerExample

# ============================================================ #

class ScanBusCallback(Nanolib.NlcScanBusCallback): # override super class
    def __init__(self):
        super().__init__()
    def callback(self, info, devicesFound, data):
        if info == Nanolib.BusScanInfo_Start :
            print('Scan started.')
        elif info == Nanolib.BusScanInfo_Progress :
            if (data & 1) == 0 :
                print('.', end='', flush=True)
        elif info == Nanolib.BusScanInfo_Finished :
            print('\nScan finished.')

        return Nanolib.ResultVoid()

callbackScanBus = ScanBusCallback() # Nanolib 2021

# ============================================================ #



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
print("nanolib setup start")
nanolib_helper.setup()
print("nanolib setup finish")

# Use Connect_motor() to connect to both motors
# the id is equivalent to the index that the device will show up as in example.py
# the id is 0 for both because after connecting to one device, the device no longer shows and index shifts left
print("connect to controller 1")
bus_hardware_ids = nanolib_helper.get_bus_hardware()
if bus_hardware_ids.empty():
    raise Exception('No bus hardware found.')
    
print('\nAvailable bus hardware:\n')

line_num = 0
# just for better overview: print out available hardware
for bus_hardware_id in bus_hardware_ids:
    print('{}. {} with protocol: {}'.format(line_num, bus_hardware_id.getName(), bus_hardware_id.getProtocol()))
    line_num += 1

print('\nPlease select (type) bus hardware number and press [ENTER]:', end ='');

line_num = int(input())
print("connected to motor 1")

print('');

if ((line_num < 0) or (line_num >= bus_hardware_ids.size())):
    raise Exception('Invalid selection!')
    
# Use the selected bus hardware
bus_hw_id = bus_hardware_ids[line_num]

# create bus hardware options for opening the hardware
bus_hw_options = nanolib_helper.create_bus_hardware_options(bus_hw_id)

# now able to open the hardware itself
nanolib_helper.open_bus_hardware(bus_hw_id, bus_hw_options)

# either scan the whole bus for devices (in case the bus supports scanning)
device_ids = nanolib_helper.scan_bus(bus_hw_id)
print("device id's: ",device_ids)

print("")
for device_id in device_ids:
    print("Found Device: {}".format(device_id.toString()))
    
if (device_ids.size() == 0):
    raise Exception('No devices found.')

print('\nAvailable devices:\n')

line_num = 0
# just for better overview: print out available hardware
for id in device_ids:
    print('{}. {} [device id: {}, hardware: {}]'.format(line_num, id.getDescription(), id.getDeviceId(), id.getBusHardwareId().getName()))
    line_num += 1

print('\nPlease select (enter) device number(0-{}) and press [ENTER]:'.format(line_num - 1), end ='');

line_num = int(input())

print('');
#motor2 = MF.connect_motor(nanolib_helper, 0)


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
#MF.move_motor(nanolib_helper, motor1, 0)
#MF.move_motor(nanolib_helper, motor2, 0)
time.sleep(3)

# Inverse Kinematic calculation
# x, y, z units are in inches
# angle units are radians
#pos_arr = kine.get_inv_kine(0, 0, 0, 0, 0, 0)
#print("pos_arr = ", pos_arr)
#pos1 = np.rad2deg(pos_arr[0])
#pos2 = np.rad2deg(pos_arr[1])





# Disconnect the motor

#nanolib_helper.disconnect_device(motor1)
#nanolib_helper.disconnect_device(motor2)

# bus_hw_id isnt accessible bc it is inside the scope of the connect_motor() function
# nanolib_helper.close_bus_hardware(bus_hw_id)

print("Closing everything successfully")
    


# NOTE: I set the object 6080h to 100 to fix the motor speed. It was originally set to 30000 and I don't know the units
#       Supposedly the units are user defined so I'm guessing it was 30000 deg/sec or smth.