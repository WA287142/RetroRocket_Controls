# Purpose of this program is to connect to all the motors and determine the order in which the motors are connected. 
# The motors are stored in variables motor1 through motor6 IN ORDER, but the actual order of the motors will not be correct. It will then iterate through each one and allow you to test which one moves
# Depending on which motor moves first, take note (e.g. motor1 moves the motor in position 4, motor2 moves the motor in position 1, etc. so the order will be something like 4,1,2,6,5,3)
# Once you've determined the actual order of connection, you need to change the variables that connect to the motors. It should look like this
# motor4 = MF.connect_motor(nanolib_helper, 0)
# motor1 = MF.connect_motor(nanolib_helper, 0)
# motor2 = MF.connect_motor(nanolib_helper, 0)
# motor6 = MF.connect_motor(nanolib_helper, 0)
# motor5 = MF.connect_motor(nanolib_helper, 0)
# motor3 = MF.connect_motor(nanolib_helper, 0)
# 
# That should give you the correct connection order of the motors for the kinematics to work properly


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
motor1 = MF.connect_motor(nanolib_helper, 0)
motor2 = MF.connect_motor(nanolib_helper, 0)
motor3 = MF.connect_motor(nanolib_helper, 0)
motor4 = MF.connect_motor(nanolib_helper, 0)
motor5 = MF.connect_motor(nanolib_helper, 0)
motor6 = MF.connect_motor(nanolib_helper, 0)


MF.setMaxSpeed(nanolib_helper, motor1, 500)
MF.setMaxSpeed(nanolib_helper, motor2, 500)
MF.setMaxSpeed(nanolib_helper, motor3, 500)
MF.setMaxSpeed(nanolib_helper, motor4, 500)
MF.setMaxSpeed(nanolib_helper, motor5, 500)
MF.setMaxSpeed(nanolib_helper, motor6, 500)

MF.setAcceleration(nanolib_helper, motor1, 1000)
MF.setAcceleration(nanolib_helper, motor2, 1000)
MF.setAcceleration(nanolib_helper, motor3, 1000)
MF.setAcceleration(nanolib_helper, motor4, 1000)
MF.setAcceleration(nanolib_helper, motor5, 1000)
MF.setAcceleration(nanolib_helper, motor6, 1000)

# object_dictionary = nanolib_helper.get_device_object_dictionary(motor1)

# Reset motor so you can change settings
# nanolib_helper.write_number_od(object_dictionary, 22, Nanolib.OdIndex(0x6040, 0x00))

# changing setting
# nanolib_helper.write_number_od(object_dictionary, 0x23, Nanolib.OdIndex(0x6098, 0x00))
# MF.move_motor(nanolib_helper, motor1, -300, 'abs')
# MF.move_motor(nanolib_helper, motor2, -300, 'abs')
# MF.move_motor(nanolib_helper, motor3, -300, 'abs')
# MF.move_motor(nanolib_helper, motor4, -300, 'abs')
# MF.move_motor(nanolib_helper, motor5, -300, 'abs')
# MF.move_motor(nanolib_helper, motor6, -300, 'abs')

# time.sleep(3)

# MF.move_motor(nanolib_helper, motor1, -1583, 'abs')
# MF.move_motor(nanolib_helper, motor2, 960, 'abs')
# MF.move_motor(nanolib_helper, motor3, 2090, 'abs')
# MF.move_motor(nanolib_helper, motor4, -210, 'abs')
# MF.move_motor(nanolib_helper, motor5, -790, 'abs')
# MF.move_motor(nanolib_helper, motor6, -630, 'abs')

print("Testing Motor 1")

val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))

while(val != -1):
    MF.move_motor(nanolib_helper, motor1, val, 'abs')
    
    val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))

print("Testing Motor 2")

val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))

while(val != -1):
    MF.move_motor(nanolib_helper, motor2, val, 'abs')
    
    val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))

print("Testing Motor 3")

val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))

while(val != -1):
    MF.move_motor(nanolib_helper, motor3, val, 'abs')
    
    val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))

print("Testing Motor 4")

val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))

while(val != -1):
    MF.move_motor(nanolib_helper, motor4, val, 'abs')
    
    val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))

print("Testing Motor 5")

val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))

while(val != -1):
    MF.move_motor(nanolib_helper, motor5, val, 'abs')
    
    val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))

print("Testing Motor 6")

val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))

while(val != -1):
    MF.move_motor(nanolib_helper, motor6, val, 'abs')
    
    val = int(input("Enter angle: Enter -1 to move to the next motor. Angles are in degrees and SHOULD (but may not) start at 0"))
