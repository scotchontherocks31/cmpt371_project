import socket

# Define server port 
PORT = 8080 #We can use any port
SERVER = socket.gethostbyname("localhost") #localhost since mac problems with socket.gethost()



#docs.python.org/3/howto/sockets.html

# Bind socket to port 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER, PORT))
server.listen(1)
print('Server is listening on port %s ...' % PORT)


#Handle incoming client request
while True:    
    # Wait for client connections
    client_conn, client_addr = server.accept()

    # Get the client request
    request = client_conn.recv(1024).decode()
    print(request)

    # Get content of test.html 
    try:
        file = open('test.html') #might need to modidify 
        content = file.read()
        file.close()

        response = 'HTTP/1.1 200 OK\n\n' + content

    except FileNotFoundError: #404 Error
        
        response = 'HTTP/1.1 404 NOT FOUND\n\n File Not Found'

    except TimeoutError: #if cannot connect

        response = 'HTTP/1.1 408 REQUEST TIME OUT\n\n Request Timed Out'

    #TODO: 304 Not Modified 

    #TODO: 400 Bad request 

    # Send HTTP response 
    client_conn.sendall(response.encode())
    client_conn.close()

# Close socket
server.close()