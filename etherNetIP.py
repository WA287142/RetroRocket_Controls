import socket
from pycomm3 import LogixDriver
import scapy


######### This file requires a server to be running prior to running this file ################
######### Need to run Server.py on a separate terminal to host the server ##################



# create a socket connection to the server
host = 'localhost'
port = 7000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

# create an instance of the driver for the Nanotec motor controller
ip_add = '192.168.1.100'
with LogixDriver(ip_add) as plc:
    # read a tag from the device
    tag_value = plc.read_tag('MyTag')

    # send the tag value over the socket connection
    sock.sendall(str(tag_value).encode())



# close the socket connection
sock.close()

