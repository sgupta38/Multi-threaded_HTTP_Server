# @Author: Sonu Gupta
# @Date: 9/4/18
# @Purpose: This file serves as a HTTP Server.
#

import os
import sys
import re
import socket
import time
from wsgiref.handlers import format_date_time
from mimetypes import MimeTypes

host = '127.0.0.1'
port = 65431

request_pattern = r'GET (?P<Resource>(.*)) HTTP/1.1'

# todo: modularize for error 404
def createHTTP_Response_header(resource_name):
    HTTP_status = 'HTTP/1.1 200 OK\r\n'
    HTTP_connection = 'Connection: Keep-Alive\r\n'   # Keeps connection alive and avoids "incomplete downloa" issue.
    date = format_date_time(time.time())
    HTTP_date = 'Date: ' + date + '\r\n'
    server = 'cs.binghamton.uni'
    HTTP_server = 'Server: ' + server + '\r\n'
    timestamp = os.path.getmtime(resource_name)
    last_modified = format_date_time(timestamp)
    HTTP_lastModified = 'Last-Modified: ' + last_modified + '\r\n'
    length = os.path.getsize(resource_name)
    HTTP_length = 'Content-Length: ' + str(length) + '\r\n'
    mime = MimeTypes()
    mime_type = mime.guess_type(resource_name)
    type = mime_type[0]
    if type is None:
        HTTP_type = 'Content-Type: None\r\n'
    else:
        HTTP_type = 'Content-Type: ' + type + '\r\n'
    HTTP_Response = HTTP_status + HTTP_date + HTTP_server + HTTP_lastModified + HTTP_length + HTTP_type + HTTP_connection + '\r\n'

    return HTTP_Response


# @note: Function used to parse the HTTP request, and get the resource which needs to be looked up in 'www' directory.
def parseRequest(request):
    pattern = re.compile(request_pattern)
    match = pattern.match(request)
    return match.group('Resource')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.bind((host, port))
sock.listen()
print('\nHTTP Server is Listening at \n')
print('Host: ', host)
print('Port: ', port)


while True:
    conn, addr = sock.accept()
    print('\nConnected to', addr)
    # receive request here
    req = conn.recv(1024);
    if req is not None:
        print('Request received is: ', req.decode('ascii'))
        rs = parseRequest(req.decode('ascii'))
        isDir = os.path.isdir('www');
        if isDir:
            ## check for presence of resource file. other wise return error 404.
            print('Need to check Resource: ', rs)
            resource = 'www' + rs
            isResource = os.path.exists(resource)
            if isResource:
                http_response_header = createHTTP_Response_header(resource)
                conn.sendall(http_response_header.encode('ascii'))
                fsendfile = open(resource, 'rb')
                data = fsendfile.read(1024)
                #data = http_response_header.encode('ascii') + data
                while data:
                    conn.sendall(data)
                    data = fsendfile.read(1024)

                fsendfile.close()
                conn.close() # after sending close socket.
                print('Send completed')
                print('Client request is served')

        else:
            print('404 error not found')
            conn.close() # after sending close socket.


