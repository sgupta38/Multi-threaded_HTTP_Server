## Multi-threaded HTTP Server


   This is a minimal HTTP server which mainly serves only **HTTP GET** requests. This server is implemented in python3 and has ability to serve multiple client requests simultaneuously. 
   Once the server is started, it listens on port 8080 and waits for client to connect. Once, the client is connected, it can request the server for specific resource with HTTP GET request. Server on the other hand, parses this received HTTP GET request, looks in resource directory i.e, **www**.
    If the resource is present, server creates the **HTTP Response Header with 200 OK** status and sends the 'Resouce'. However, if resource is not present, server returns **HTTP Response header with 404 Error Not Found** status.
	
### Implementation
---
 - Directory **www** acts as a **Resource Directory**. When server is started, it first looks for the resource directory. If its not present, it quits. Function `os.path.isdir('xxx')` handles this part.
 - If resource directory is present, Server waits for clients to connect.
 - Once, the client is connected, a new thread is spwaned which takes care of that client here on-wards. Each thread executes function `handleClientConncetion()`.
 - Client sends the HTTP GET request. Server on the other hand, parses this request using Regular expression to get the name of resource.  Function `parseRequest()` is used for parsing the request.
 - Server looks for the resource in resource directory. If its present, it creates the ***`'HTTP Response' header with status 200 OK`*** and then sends it to the client along with resource. Function `createHTTP_Response_header()` is used for creating HTTP response header.
 - For every resource, a `'global variable xxxCount'` is maintained which counts the number of times the resource is requested by client.
 - If resource does not exit in resource directory, ***`'HTTP Response' header with status 404 Error Not Found`*** is sent to the client. Function `sendResourceNotFound()` is used for this purpose.
 - After sending the 'HTTP Response' to repective client, server closes the socket connection.
 
 ### How to Run?
 ---
 **Server End:**
 
Makefile is maintained for calling the server program.

Just type 'make' on terminal. 

`>make`
		
make internally calls `python3 HTTPServer.py`

****Client End:****

'Web browsers' / 'wget' utility can be used for HTTP GET requests.

***For web browsers***: Simply type following URL-
			

    http://127.0.0.1:8080/test.html
			
***For wget***: Type following comment.
		
	wget http://127.0.0.1:8080/test.html
			
### Sample Input/Output:
---

