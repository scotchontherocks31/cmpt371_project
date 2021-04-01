# code goes here, or in multiple places

#HOW TO RUN
#After installing dependecies do python3 shell.py
#Open up your preferred browser and enter in the search bar: localhost:PORT
#where PORT is the port used in the PORT variable


#Codes given -----
#200 OK
#304 Not Modified
#400 Bad Request
#404 Not Found
#408 Request Timed Out 


#If these aren't installed on your machine, pip install beforehand
import http.server
import socketserver

PORT = 8080 #This is just the port i was using, feel free to use any post

#Potential User Bug 1: OSError: [Errno 48] Address already in use
#If this is the case you can either switch ports or what i do is suspend all terminal tasks
#This will end the terminal tasks and close your ports (also good security)


#We are using a custom class since our file isnt called index.html
#This class (http.server.SimpleHTTPRequestHandler) also lets us to see if directory specified
#CGIHTTPRequest allows us to do stuff like POST See documentation for more
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'test.html' #Use test.html instead of finding index.html since if not found displays a tree
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyHttpRequestHandler #Make handler our custom class instead of default

#To instantiate a TCP server we need the address and handler used, TCP is tuple of ipaddress, port
#empty string ip -> listen on any network interface
#PORT -> listen to what port
with socketserver.TCPServer(("",PORT), Handler) as httpd: 
    print(f"Running Port is: {PORT} ") #print in terminal (confirm its running)
    httpd.serve_forever() #Serve_forever allows the server to start and respond to requests
