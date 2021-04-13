import socket
from datetime import datetime
from pathlib import Path
import time

#specify server address
PORT = 8080
SERVER = socket.gethostbyname("localhost")

#create TCP welcoming socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the server port to the socket
server.bind((SERVER, PORT))

#server begins listerning foor incoming TCP connections
server.listen(1)
print(f"Server is listening on port {PORT}")

# set the waitUntilTimeout---->(alterable)
waitUntilTimeOut = 10000  # Original set value: 10000

modify = 0 
while True:
    beginTime = time.time()
    #server waits on accept for incoming requests.
    #New socket created on return
    client_conn, client_addr = server.accept()

    # 408 Request Time Out
    if time.time() - beginTime > waitUntilTimeOut:
        request = client_conn.recv(1024).decode('utf-8')
        response = 'HTTP/1.1 408 REQUEST TIMED OUT\n\n'
    else:    
   
        #Read from socket
        request = client_conn.recv(1024).decode('utf-8')
        string_list = request.split(' ')     # Split request from spaces

        if 'GET' in string_list:
            method = string_list[0]
            #print(string_list)
            requesting_file = string_list[1]
            print('Client request ',requesting_file)
            myfile = requesting_file.split('?')[0] 
            myfile = myfile.strip('/')
            if(myfile == ''):
                myfile = 'test.html'

            try:
                myfilePath = Path(myfile)
                file = open(myfile)
                content = file.read()
                file.close()
                if(modify != myfilePath.stat().st_mtime):
                    modify = myfilePath.stat().st_mtime
                    response = 'HTTP/1.1 200 OK\n\n' + content
                    print("200 OK")
                
                else:
                    response = 'HTTP/1.1 304 NOT MODIFIED\n\n' + content
                    print("300 NOT MODIFIED")

            except FileNotFoundError:
                response = 'HTTP/1.1 404 NOT FOUND\n\n File Not Found'
                print("404 NOT FOUND")

        #400 Bad Request
        else:
            response = 'HTTP/1.1 400 BAD REQUEST\n\n'
            print("400 BAD REQUEST") 

        print(request)
        client_conn.sendall(response.encode())
        client_conn.close()

    
server.close()
