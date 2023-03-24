import sys
sys.path.insert(8, r'C:\Users\Public\Downloads\NanoLib_1.0.1\NanoLib_Python_Windows\nanotec_nanolib_win-1.0.1\nanotec_nanolib')

from nanotec_nanolib import Nanolib
from nanolib_helper import NanolibHelper
from nanolib_profinet_example import ProfinetExample
from nanolib_sampler_example import SamplerExample

nanolib_helper = NanolibHelper()

# create access to the nanolib
nanolib_helper.setup()
    
print('Nanolib Example')

 # list all hardware available, decide for the first one
bus_hardware_ids = nanolib_helper.get_bus_hardware()

# Use the selected bus hardware
bus_hw_id = bus_hardware_ids[4]

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

print('\nPlease select (enter) device number(0-{}) and press [ENTER]:'.format(line_num - 1), end ='');

line_num = int(input())

print('');
if ((line_num < 0) or (line_num >= device_ids.size())):
    raise Exception('Invalid selection!')

# We can create the device id manually    
# device_id = Nanolib.DeviceId(bus_hw_id, 1, "")
# or select first found device on the bus
device_id = device_ids[line_num]

device_handle = nanolib_helper.create_device(device_id)

# now connect to the device
nanolib_helper.connect_device(device_handle)

object_dictionary = nanolib_helper.get_device_object_dictionary(device_handle)

print("Obj Dict: ", object_dictionary)


print('Motor Stop (0x6040-0)')
status_word = nanolib_helper.write_number_od(object_dictionary, 6, Nanolib.OdIndex(0x6040, 0x00))




# # Create the motor object and its desired connection
# motor = Nanolib.Motor("EtherCAT_TCP", host="192.168.1.166")

# # Initialize the motor
# motor.init()

# motor.set_pos(1000)
# motor.move_abs()

# from pycomm3 import *

# # create a connection to the motor controller
# motor = SLCDriver('192.168.1.166',init_tags=True)
# print("Motor object created")

# print(motor.connected)

# motor.get_tag_list()
# read the position of the motor from tag 'Motor1_Position'
# position = motor.read_tag('Motor1_Position')

# close the connection to the motor controller
# motor.close()
