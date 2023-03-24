# import sys
# sys.path.insert(8, r'C:\Users\Public\Downloads\NanoLib_1.0.1\NanoLib_Python_Windows\nanotec_nanolib_win-1.0.1\nanotec_nanolib')

# from nanotec_nanolib import Nanolib
# from nanolib_helper import NanolibHelper
# from nanolib_profinet_example import ProfinetExample
# from nanolib_sampler_example import SamplerExample


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

from pylogix import PLC
with PLC() as comm:
    comm.IPAddress = '192.168.1.166'
    # ret = comm.Read('MyTagName')
    # print(ret.TagName, ret.Value, ret.Status)
    tags = comm.GetTagList()
    for t in tags.Value:
        print(t.TagName, t.DataType)
        