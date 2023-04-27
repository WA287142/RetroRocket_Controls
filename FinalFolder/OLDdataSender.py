# This program is used to connect to a server and send data as a test. This is to simulate
# the VR simulation data connection.
import pickle
import socket
import time

f = open("three_sweep.txt", "r")

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
port = 7000
server_address = ('127.0.0.1', port)

client_socket.connect(server_address)

# data = input("Enter data: ")
# while data != 'stop':
    
#     client_socket.send(data.encode())
#     data = input("Enter data:")
#     msg = client_socket.recv(1024)
#     print(msg.decode())
f.readline()    # Remove the first line which is labels

input = f.readline()

while input:
    # data = input.split(',')
    data = pickle.dumps(input)
    client_socket.send(data)
    input = f.readline()
    msg = client_socket.recv(1024)
    print(msg.decode())

client_socket.send()
print("Closing connection")
client_socket.close()
