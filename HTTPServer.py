# @Author: Sonu Gupta
# @Date: 9/4/18
# @Purpose: This file serves as a HTTP Server which.
#

import sys
import socket

host = '127.0.0.1'
port = 65431

# Response will be standard HTTP Response header.
# @todo: Need to change content-type, since we are sending file.
response = """
Status: 200 OK
Content-type: text/html
"""

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.bind((host, port))
sock.listen()
print("\nHTTP Server is Listening at \n")
print("Host: ", host)
print("Port: ", port)

conn, addr = sock.accept()

print('\nConnected to', addr)

while True:
    # receive request here
    data = conn.recv(1024);
    if data is not None:
        print("Request received is: ", data.decode('ascii'))
        # parse request shall go here, and send response back to client
        # todo: parsing , logic for 'www' directory.
        conn.sendall(response.encode('ascii'))
        conn.close()
    break

print('client request is served')