# -*- coding: utf-8 -*-
# Use this program to connect to a single motor and test it #
import sys
sys.path.insert(8, r'C:\Users\Public\Downloads\NanoLib_1.0.1\NanoLib_Python_Windows\nanotec_nanolib_win-1.0.1\nanotec_nanolib')

from nanotec_nanolib import Nanolib
from nanolib_helper import NanolibHelper
from nanolib_profinet_example import ProfinetExample
from nanolib_sampler_example import SamplerExample

def askUser(question):
    userInput = input("" + str(question) + " " + "[Y/N]:" + " ")
    userInput = str(userInput).strip().upper()
    if(userInput == "Y"):
        return True
    else:
        return False

def object_code_to_string(object_code):
    return {
        Nanolib.ObjectCode_Null: 'Null',
        Nanolib.ObjectCode_Deftype: 'Deftype',
        Nanolib.ObjectCode_Defstruct: 'Defstruct',
        Nanolib.ObjectCode_Var: 'Var',
        Nanolib.ObjectCode_Array: 'Array',
        Nanolib.ObjectCode_Record: 'Record'
        }.get(object_code, 'Unknown')


def object_dictionary_access_examples(nanolib_helper, device_handle):
    print('\nOD Example\n')

    print("Reading subindex 0 of index 0x6040")
    status_word = nanolib_helper.read_number(device_handle, Nanolib.OdIndex(0x6040, 0x00))
    print('Result: {}\n'.format(status_word))

    print('Motor Stop (0x6040-0)')
    status_word = nanolib_helper.write_number(device_handle, 6, Nanolib.OdIndex(0x6040, 0x00), 16)

    print('\nRead Nanotec home page string')
    home_page = nanolib_helper.read_string(device_handle, Nanolib.OdIndex(0x6505, 0x00))
    print('The home page of Nanotec Electronic GmbH & Co. KG is: {}'.format(home_page))

    print('\nRead device error stack')
    error_stack = nanolib_helper.read_array(device_handle, Nanolib.OdIndex(0x1003, 0x00))
    print('The error stack has {} elements\n'.format(error_stack[0]))

###################################################################################################################################################
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
    nanolib_helper.write_number_od(object_dictionary, 22, Nanolib.OdIndex(0x6040, 0x00))
    print("Controls")
    print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x6040, 0x00)))
    
    # Set the units for the motor
    # degrees = 41h
    nanolib_helper.write_number_od(object_dictionary, 0x00410000, Nanolib.OdIndex(0x60A8, 0x00))
    print("Units")
    print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x60A8, 0x00)))

    # Set the Target Position 
    nanolib_helper.write_number_od(object_dictionary, value, Nanolib.OdIndex(0x607A, 0x00))

    print("Target Position")
    print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x607A, 0x00)))

    # Set the units (m, in, ft)
    #nanolib_helper.write_number_od(object_dictionary, 1, Nanolib.OdIndex(0x6060, 0x00))

    # Set the Controls
    # 10110 = 22 -> Use this value to reset the motor so you can update target position
    # 11111 = 31 -> You want this to run your motor
    # 1111 = 15
    # 111111 = 63
    # 1011111 = 95
    nanolib_helper.write_number_od(object_dictionary, 31, Nanolib.OdIndex(0x6040, 0x00))
    print("Final Controls")
    print(nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x6040, 0x00)))


###################################################################################################################################################

def object_dictionary_access_examples_via_dictionary_interface(nanolib_helper, device_handle):
    home_page_od = Nanolib.OdIndex(0x6505, 0x00);
    control_word_od = Nanolib.OdIndex(0x6040, 0x00);

    print('\nOD Example via Dictionary Interface\n')

    object_dictionary = nanolib_helper.get_device_object_dictionary(device_handle)

    print("Reading subindex 0 of index 0x6040")
    status_word = nanolib_helper.read_number_od(object_dictionary, Nanolib.OdIndex(0x6040, 0x00))
    print('Result: {}\n'.format(status_word))

    print('Motor Stop (0x6040-0)')
    status_word = nanolib_helper.write_number_od(object_dictionary, 6, Nanolib.OdIndex(0x6040, 0x00))

    print('\nRead Nanotec home page string')
    home_page = nanolib_helper.read_string_od(object_dictionary, home_page_od)
    print('The home page of Nanotec Electronic GmbH & Co. KG is: {}'.format(home_page))
    
    object_entry = nanolib_helper.get_object_entry(object_dictionary, control_word_od.getIndex())
    print('Some ObjectEntry properties:')
    print('Object(0x%04X).ObjectCode = %s' % (control_word_od.getIndex(), object_code_to_string(object_entry.getObjectCode())))
    print('Object(0x%04X).DataType = %s' % (control_word_od.getIndex(), Nanolib.OdTypesHelper.objectEntryDataTypeToString(object_entry.getDataType())))

    print('Some ObjectSubEntry properties:')
    object_sub_entry = nanolib_helper.get_object(object_dictionary, control_word_od);
    print('OdIndex(0x%04X:%02X).DataType = %s' % (control_word_od.getIndex(), control_word_od.getSubIndex(), Nanolib.OdTypesHelper.objectEntryDataTypeToString(object_sub_entry.getDataType())))
    print('OdIndex(0x%04X:%02X).BitLength = %d' %(control_word_od.getIndex(), control_word_od.getSubIndex(), object_sub_entry.getBitLength()))


################################### Start of Code #######################################

if __name__ == '__main__':
    nanolib_helper = NanolibHelper()

    # create access to the nanolib
    nanolib_helper.setup()
    
    print('Nanolib Example')

    # its possible to set the logging level to a different level
    nanolib_helper.set_logging_level(Nanolib.LogLevel_Off)

    # list all hardware available, decide for the first one
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

    # move_motor(nanolib_helper, device_handle, 0)

    # Allows User to input desired angle for both motors until -1 is entered

    print("Setting acceleration to ", 50)
    
    object_dictionary = nanolib_helper.get_device_object_dictionary(device_handle)
    
    nanolib_helper.write_number_od(object_dictionary, 22, Nanolib.OdIndex(0x6040, 0x00))
    nanolib_helper.write_number_od(object_dictionary, 50, Nanolib.OdIndex(0x60C5, 0x00))

    val = int(input("Enter angle: "))

    while(val != -1):
        move_motor(nanolib_helper, device_handle, val)
      
        val = int(input("Enter angle: "))
    # now ready to work with the controller, here are some examples on how to access the
    # object dictionary:
    # object_dictionary_access_examples(nanolib_helper, device_handle)
    # object_dictionary_access_examples_via_dictionary_interface(nanolib_helper, device_handle)

    # if(bus_hw_id.getBusHardware() == Nanolib.BUS_HARDWARE_ID_NETWORK):
    #     profinet_dcp_interface = nanolib_helper.get_profinet_dcp_interface()
    #     if(
    #         profinet_dcp_interface.isServiceAvailable(bus_hw_id).hasError() == False
    #     ):
    #         if(askUser("Do you wish to proceed with Profinet DCP example?")):
    #             profinetExample = ProfinetExample(bus_hw_id, profinet_dcp_interface)
    #             profinetExample.execute()
        
    # if(askUser("Do you wish to proceed with sampler examples?")):
    #     # samplerExample = SamplerExample(device_handle, nanolib_helper)
    #     # print("")
    #     # samplerExample.executeWithoutCallback()
    #     # samplerExample.executeWithCallback()
    #     upNanoJ = Nanolib.NanoLibAccessor.uploadNanoJFromFile(bus_hw_id,device_handle, r"C:\Users\Public\Downloads\Example_1_Velocity_Mode\vmmcode.cpp", Nanolib.NlcCallback.callback(bus_hw_id))






    # cleanup and close everything
    nanolib_helper.disconnect_device(device_handle)
    nanolib_helper.close_bus_hardware(bus_hw_id)

    print("Closing everything successfully")
