import socket
from pycomm3 import LogixDriver
import scapy


######### This file requires a server to be running prior to running this file ################
######### Need to run Server.py on a separate terminal to host the server ##################


print("TEst")
# create a socket connection to the server
# host = 'localhost'
# port = 7000
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((host, port))

# create an instance of the driver for the Nanotec motor controller
ip_address = '169.254.89.103'
print("IP Address")
# with LogixDriver(ip_address) as plc:
#     print("LogixDriver")

#     tags = plc.read('MyTag1', 'MyTag2', 'MyTag3')
#     print(tags)
#     # Get the tag list
#     plc.read('dint_tag')

#     # read a tag from the device
#     #tag_value = plc.read_tag('MyTag')

#     # send the tag value over the socket connection
#     #sock.sendall(str(tag_value).encode())

plc = LogixDriver(ip_address, 44818)

plc.open()
print("LogixDriver made")

plc.get_tag_list()    

plc.close()

# close the socket connection
#sock.close()
