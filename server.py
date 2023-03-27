import socket
import nanotec_nanolib

try:
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # AF_INET is the address-family ipv4
        # SOCK_STREAM is connection oriented TCP protocol
except socket.error as err:
    print("Server creation failed: %s" %(err))

# set the socket options to allow multiple connections
serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# ip = socket.gethostbyname('www.google.com')
#     # obtaining the ip address
# print(ip)

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

    # while True:
    #     data = conn.recv(4096)  # 4096 is number of bytes transferred. Might be an issue
    #     if not data:
    #         break
    #     from_client += data
    #     print(from_client)

    #     conn.send("Message from Server\n")

    while True:
        data = conn.recv(4096)
        if not data:
            break
        
        print ("Client says: "+data.decode())

        conn.sendall('Server received message'.encode())


    conn.close()
    print('client disconnected')

    break