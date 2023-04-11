# This program is a module of necessary motor functions needed to use a Nanotec Motor controller

import sys
import socket
import time
sys.path.insert(8, r'C:\Users\Public\Downloads\NanoLib_1.0.1\NanoLib_Python_Windows\nanotec_nanolib_win-1.0.1\nanotec_nanolib')


from nanotec_nanolib import Nanolib
from nanolib_helper import NanolibHelper
from nanolib_profinet_example import ProfinetExample
from nanolib_sampler_example import SamplerExample

# NOTE: Each digit of hex is 4 bits.

# For object 6040h,
    # Bit 4 - start travel command by setting it to 1
    # Bit 5 - a travel command triggered by bit 4 is executed
    # Bit 6 - at value 0, the target position 607Ah is absolute
    #       - at value 1, target position 607Ah is relative
    # Bit 8 - at value 1, motor stops
# Need to change object index 6060h to 1 for Profile Position Mode

# Set the max motor speed
def setMaxSpeed(nanolib_helper, device_handle, maxSpeed):
    print("Setting max motor speed to ", maxSpeed)
    
    object_dictionary = nanolib_helper.get_device_object_dictionary(device_handle)

    nanolib_helper.write_number_od(object_dictionary, 22, Nanolib.OdIndex(0x6040, 0x00))
    nanolib_helper.write_number_od(object_dictionary, maxSpeed, Nanolib.OdIndex(0x6080, 0x00))
    
# Move the motor. value - the position or distance to move to
#                 relative - if 1, position is relative. otherwise position is absolute
def move_motor(nanolib_helper, device_handle, value, mode):
    print("Moving Motor to angle: ", value)
    home_page_od = Nanolib.OdIndex(0x6505, 0x00);
    control_word_od = Nanolib.OdIndex(0x6040, 0x00);

    object_dictionary = nanolib_helper.get_device_object_dictionary(device_handle)
    
    # Setting the Mode of Operation to Profile Position Mode
    # You may need this to set the controller mode the first time you run it
    #nanolib_helper.write_number_od(object_dictionary, 1, Nanolib.OdIndex(0x6060, 0x00))

    # Make sure motor starts out as off by resetting motor controls
    # 10110 = 22 -> Use this value to reset the motor so you can update target position
    nanolib_helper.write_number_od(object_dictionary, 22, Nanolib.OdIndex(0x6040, 0x00))
    # print("Controls")
    # print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x6040, 0x00)))
    
    # Set the units for the motor. Value for Degrees = 41h
    # First 16 bits are reserved values and each hex digit is 4 bits
    nanolib_helper.write_number_od(object_dictionary, 0x00410000, Nanolib.OdIndex(0x60A8, 0x00))
    # print("Units")
    # print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x60A8, 0x00)))

    # Set the Target Position (000001388 is 5000)
    nanolib_helper.write_number_od(object_dictionary, value, Nanolib.OdIndex(0x607A, 0x00))

    # print("Target Position")
    # print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x607A, 0x00)))

    # Set the Controls
    # 10110 = 22 -> Use this value to reset the motor so you can update target position
    # 11111 = 31 -> You want this to run your motor
    # 1111 = 15
    # 111111 = 63
    # 1011111 = 95 -> This is for running the motor in relative position
    if mode == 'rel':  
        nanolib_helper.write_number_od(object_dictionary, 95, Nanolib.OdIndex(0x6040, 0x00))
    elif mode == 'abs':
        nanolib_helper.write_number_od(object_dictionary, 31, Nanolib.OdIndex(0x6040, 0x00))
    else:
        # Exits the program if an invalid position mode is selected
        print("invalid position mode. Needs to be 'abs' or 'rel'")
        sys.exit()
    # print("Final Controls")
    # print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x6040, 0x00)))

# Connect motor needs nanolib_helper and the device # of the motor (ex. 0, 1, 2)
def connect_motor(nanolib_helper, motorID):
    # list all hardware available, decide for the first one
    bus_hardware_ids = nanolib_helper.get_bus_hardware()
    line_num = 0
    for bus_hardware_id in bus_hardware_ids:
            print('{}. {} with protocol: {}'.format(line_num, bus_hardware_id.getName(), bus_hardware_id.getProtocol()))
            line_num += 1
        
    # Use the selected bus hardware
    # 6 is the USB connection. May change as more motors are connected
    ############ NEED TO CHECK WITH THE NUMEBR OF INPUTS ###############
    bus_hw_id = bus_hardware_ids[10]

    # create bus hardware options for opening the hardware
    bus_hw_options = nanolib_helper.create_bus_hardware_options(bus_hw_id)

    # now able to open the hardware itself
    nanolib_helper.open_bus_hardware(bus_hw_id, bus_hw_options)

    # either scan the whole bus for devices (in case the bus supports scanning)
    device_ids = nanolib_helper.scan_bus(bus_hw_id)

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

    # Select Device on Bus
    device_id = device_ids[motorID]
    

    device_handle = nanolib_helper.create_device(device_id)
    print("Device Handle:", device_handle)

    # now connect to the device
    nanolib_helper.connect_device(device_handle)

    object_dictionary = nanolib_helper.get_device_object_dictionary(device_handle)

    # Setting the Mode of Operation to Profile Position Mode
    # You may need this to set the controller mode the first time you run it
    nanolib_helper.write_number_od(object_dictionary, 1, Nanolib.OdIndex(0x6060, 0x00))

    # print("Motor ", motorID, " Object Dictionary: ", object_dictionary)

    # device_handle is used to call the connection to the motor
    return device_handle