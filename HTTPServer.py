# @Author: Sonu Gupta
# @Date: 9/4/18
# @Purpose: This file serves as a HTTP Server. Currently, it is supporting only 'HTTP GET' requests.
#           

import os
import sys
import re
import socket
import time
import threading
from mimetypes import MimeTypes
from wsgiref.handlers import format_date_time

# Global variables
pdfCount = 0;
pageCount = 0;
imageCount = 0;
packageCount = 0;
port = 8080
host = '127.0.0.1'

# Regular expression to parse HTTP GET request and get resource name
request_pattern = r'GET /(?P<Resource>(.*)) HTTP/1.1'

# HTTP Response header functions.

def getHTTPDate():
    date = format_date_time(time.time())
    http_date = 'Date: ' + date + '\r\n'
    return http_date

def getHTTPStatus(code):
    if code == 200:
        return 'HTTP/1.1 200 OK\r\n'
    else:
        return 'HTTP/1.1 404 Not Found\r\n'

def getServerName():
    server = 'cs.binghamton.uni'
    return 'Server: ' + server + '\r\n'

def getLastModifiedTime(resource_path):
    timestamp = os.path.getmtime(resource_path)
    last_modified = format_date_time(timestamp)
    return 'Last-Modified: ' + last_modified + '\r\n'

def getContentLength(resource_path):
    length = os.path.getsize(resource_path)
    return 'Content-Length: ' + str(length) + '\r\n'

def getContentType(resource_path):
    mime = MimeTypes()
    mime_type = mime.guess_type(resource_path)
    type = mime_type[0]
    if type is None:
        return 'Content-Type: None\r\n'
    else:
        return 'Content-Type: ' + type + '\r\n'

def getHTTPConnection():
    return 'Connection: Keep-Alive\r\n' # Keeps connection alive and avoids "incomplete downloa" issue.

# Method to create final 'HTTP Response' header.
def createHTTP_Response_header(resource_name, code):
    try:
        if code == 404:
            resource_name = 'www/404.html'

        HTTP_Response = getHTTPStatus(code) + \
                        getHTTPDate() + \
                        getServerName() + \
                        getContentLength(resource_name) + \
                        getContentType(resource_name) + \
                        getHTTPConnection()

        if code == 200:
            HTTP_Response += getLastModifiedTime(resource_name)  # Only existing resource has modified time
    
        HTTP_Response += '\r\n'  # Adding blank line

        return HTTP_Response

    except:
        print("Some error occured in createHTTP_Response_header()")
        return ''

# Function to parse the regular expression.
def parseRequest(request):
    try:
        pattern = re.compile(request_pattern)
        match = pattern.match(request)
        if match is None:
            return ''
        else:
            return match.group('Resource')
    except:
        print("Some error occured in parseRequest()")
        return ''
# Function to send the 'Resource file' to connected client
def sendResourceFile(conn, res_file, code):
    try:
        if code == 404:
            res_file = 'www/404.html'

        res_file = open(res_file, 'rb')
        data = res_file.read(1024)
        while data:
            conn.send(data)
            data = res_file.read(1024)

        res_file.close()
        return True
    except:
        print("Some error occured in sendResourceFile()")
        res_file.close()
        return False

# Function to send '404.html' in case of failures.
def sendResourceNotFound(conn):
    try:
        resource = 'www/404.html'
        http_response_header = createHTTP_Response_header(resource, 404)
        conn.sendall(http_response_header.encode('ascii'))
        sendResourceFile(conn, resource, 404)
        print('404 error not found')
    except:
        print("Some Internal error occured:: Request Error")
    finally:
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()

# Function to print the 'resource info'
def printResourceInfo(addr, rs, count):
     print('/' + rs + ' | ' + str(addr[0]) + ' | ' + str(addr[1]) + ' | ' + str(count))

# 'Thread fuction' called for each client connection
def handleClientConncetion(conn, addr):
    global pageCount, pdfCount , packageCount , imageCount
    #print('Thread id: ', threading.get_ident())
    req = conn.recv(1024);
    if req:
        rs = parseRequest(req.decode('ascii'))

        if rs:
            if rs == 'test.html':
                pageCount += 1
                printResourceInfo(addr, rs, pageCount)

            elif rs == 'pdf-sample.pdf':
                pdfCount += 1
                printResourceInfo(addr, rs, pdfCount)

            elif rs == 'lena_std.tif':
                imageCount +=1
                printResourceInfo(addr, rs, imageCount)

            elif rs == 'skype-ubuntu-precise_4.3.0.37-1_i386.deb':
                packageCount += 1
                printResourceInfo(addr, rs, packageCount)

            resource = 'www/' + rs
            isResource = os.path.exists(resource)

            if(isResource):
                code = 200   # if resource found in 'www'
            else:
                code = 404   # if resource not found in 'www'
            try:
                http_response_header = createHTTP_Response_header(resource, code)
                conn.sendall(http_response_header.encode('ascii'))
                sendResourceFile(conn, resource, code)
            except:
                print("Some Internal error occured:: Resource Not Found")
            finally:
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
        else:
            sendResourceNotFound(conn)

    else: # For invalid requests
        sendResourceNotFound(conn)

    return True

## Main Function of HTTP Server. Creates socket, binds and listens for client connections.
def main():
    isDir = os.path.isdir('www')
    if isDir is False:
        print("Resource directory 'www' does not exist. Quitting the server.")
        os._exit(1)

    sock = socket.socket();
    sock.bind((host, port))
    sock.listen()
    print('\nHTTP Server is Running on \n')
    print('Host Name: ', host)
    print('Port Number: ', port)
    print('')

    while True:
        conn, addr = sock.accept()
        # spawn new thread here
        threading.Thread(target = handleClientConncetion, args=(conn, addr,)).start()

# Main routine starts here
main()
sock.close()
