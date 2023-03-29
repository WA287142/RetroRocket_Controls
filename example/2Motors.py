import sys
import socket
sys.path.insert(8, r'C:\Users\Public\Downloads\NanoLib_1.0.1\NanoLib_Python_Windows\nanotec_nanolib_win-1.0.1\nanotec_nanolib')

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
# NOTE: Each digit of hex is 4 bits.

# For object 6040h,
    # Bit 4 - start travel command by setting it to 1
    # Bit 5 - a travel command triggered by bit 4 is executed
    # Bit 6 - at value 0, the target position 607Ah is absolute
    #       - at value 1, target position 607Ah is relative
    # Bit 8 - at value 1, motor stops
# Need to change object index 6060h to 1 for Profile Position Mode

def move_motor(nanolib_helper, device_handle, value):
    print("Moving Motor")
    home_page_od = Nanolib.OdIndex(0x6505, 0x00);
    control_word_od = Nanolib.OdIndex(0x6040, 0x00);

    object_dictionary = nanolib_helper.get_device_object_dictionary(device_handle)
    
    # Setting the Mode of Operation to Profile Position Mode
    nanolib_helper.write_number_od(object_dictionary, 1, Nanolib.OdIndex(0x6060, 0x00))

    # Make sure motor starts out as off by resetting motor controls
    # 10110 = 22 -> Use this value to reset the motor so you can update target position
    nanolib_helper.write_number_od(object_dictionary, 22, Nanolib.OdIndex(0x6040, 0x00))
    print("Controls")
    print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x6040, 0x00)))
    
    # Set the units for the motor. Value for Degrees = 41h
    # First 16 bits are reserved values
    nanolib_helper.write_number_od(object_dictionary, 0x00410000, Nanolib.OdIndex(0x60A8, 0x00))
    print("Units")
    print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x60A8, 0x00)))

    # Set the Target Position (000001388 is 5000)
    nanolib_helper.write_number_od(object_dictionary, value, Nanolib.OdIndex(0x607A, 0x00))

    print("Target Position")
    print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x607A, 0x00)))

    # Set the Controls
    # 10110 = 22 -> Use this value to reset the motor so you can update target position
    # 11111 = 31 -> You want this to run your motor
    # 1111 = 15
    # 111111 = 63
    # 1011111 = 95
    nanolib_helper.write_number_od(object_dictionary, 31, Nanolib.OdIndex(0x6040, 0x00))
    print("Final Controls")
    print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x6040, 0x00)))

# Connect motor needs nanolib_helper and the device # of the motor (ex. 0, 1, 2)
def connect_motor(nanolib_helper, motorID):
    # list all hardware available, decide for the first one
    bus_hardware_ids = nanolib_helper.get_bus_hardware()

    line_num = 0
    for bus_hardware_id in bus_hardware_ids:
            print('{}. {} with protocol: {}'.format(line_num, bus_hardware_id.getName(), bus_hardware_id.getProtocol()))
            line_num += 1
        
    # Use the selected bus hardware
    # 5 is the USB connection
    bus_hw_id = bus_hardware_ids[6]

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

    # now connect to the device
    nanolib_helper.connect_device(device_handle)

    object_dictionary = nanolib_helper.get_device_object_dictionary(device_handle)

    print("Motor ", motorID, " Object Dictionary: ", object_dictionary)

    return device_handle






################################################# MAIN ####################################

nanolib_helper = NanolibHelper()

# create access to the nanolib
nanolib_helper.setup()

##### Everything in this section below should be turned into a function for better readability #####
# Uncomment this section if the connect_motor() does not work. This section is proven to work

"""# list all hardware available, decide for the first one
 bus_hardware_ids = nanolib_helper.get_bus_hardware()

line_num = 0
for bus_hardware_id in bus_hardware_ids:
        print('{}. {} with protocol: {}'.format(line_num, bus_hardware_id.getName(), bus_hardware_id.getProtocol()))
        line_num += 1
    
# Use the selected bus hardware
# 5 is the USB connection
bus_hw_id = bus_hardware_ids[6]

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

# Changed this to take in two motor devices ####
device1_id = device_ids[0]
device2_id = device_ids[1]

device1_handle = nanolib_helper.create_device(device1_id)
device2_handle = nanolib_helper.create_device(device2_id)


# now connect to the device
nanolib_helper.connect_device(device1_handle)
nanolib_helper.connect_device(device2_handle)


object_dictionary1 = nanolib_helper.get_device_object_dictionary(device1_handle)
object_dictionary2 = nanolib_helper.get_device_object_dictionary(device2_handle)


print("Controller 1 Obj Dict: ", object_dictionary1)
print("")
print("Controller 2 Obj Dict: ", object_dictionary1) """

###############################################################################

# Use Connect_motor() to connect to both motors
# the id is equivalent to the index that the device will show up as in example.py
motor1 = connect_motor(nanolib_helper, 0)
motor2 = connect_motor(nanolib_helper, 1)

# Allows User to input desired angle for both motors until -1 is entered

# val = int(input("Enter angle: "))

# while(val != -1):
#     move_motor(nanolib_helper, device1_handle, val)
#     move_motor(nanolib_helper, device2_handle, val)
#     val = int(input("Enter angle: "))
# ###############################################################################

# ###############################################################################
# Runs through 360 degrees of motion in 1 degree increments
for i in range(1,361):
    move_motor(nanolib_helper, motor1, i)
    move_motor(nanolib_helper, motor2, i)


# Disconnect the motor

nanolib_helper.disconnect_device(motor1)
nanolib_helper.disconnect_device(motor2)

# bus_hw_id isnt accessible bc it is inside the scope of the connect_motor() function
# nanolib_helper.close_bus_hardware(bus_hw_id)

print("Closing everything successfully")
    