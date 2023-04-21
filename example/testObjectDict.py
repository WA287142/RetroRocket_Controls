# Purpose of this program is to change object dictionary values to test their functionality

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

MF.setMaxSpeed(nanolib_helper, motor1, 500)
MF.setAcceleration(nanolib_helper, motor1, 1000)
object_dictionary = nanolib_helper.get_device_object_dictionary(motor1)

# Reset motot so you can change settings
# nanolib_helper.write_number_od(object_dictionary, 22, Nanolib.OdIndex(0x6040, 0x00))

# changing setting
# nanolib_helper.write_number_od(object_dictionary, 0x23, Nanolib.OdIndex(0x6098, 0x00))

MF.move_motor(nanolib_helper, motor1, 0, 'abs')

val = int(input("Enter angle: "))

while(val != -1):
    MF.move_motor(nanolib_helper, motor1, val, 'abs')
    
    val = int(input("Enter angle: "))
