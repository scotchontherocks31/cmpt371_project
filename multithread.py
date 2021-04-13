from socket import *
import threading
import os
from _thread import *
import time
from pathlib import Path

HOST = gethostbyname("localhost")
PORT = 8080
CWD = os.getcwd()
PRINT_LOCK = threading.Lock()
time_limit = 10000  # Original set value: 10000

class ClientThread(threading.Thread):
    def __init__(self, client_addr, client_sock, time):
        threading.Thread.__init__(self)
        self.client_sock = client_sock
        self.client_addr = client_addr
        self.time = time
        self.MODIFY_CHECK = 0
        print("\nNew connection added at: ", client_addr)

    def run(self):
        print("\nConnection from: ", self.client_addr)

        while True:
            
            # ERROR 408 CHECK
            if (time.time() - self.time) >= time_limit:
                #decode request
                try:
                    request = self.client_sock.recv(1024).decode()
                except OSError:
                    break
                #produce response
                response = 'HTTP/1.1 408 REQUEST TIMED OUT\n\n'

            else:
                #decode request
                try:
                    request = self.client_sock.recv(1024).decode()
                    print("\n\tPrinting request: ")
                    print(request)
                except OSError:
                    break
                
                string_line = request.split(' ')
                
                # ERROR 400 CHECK
                if 'GET' in string_line: 
                    request_file = string_line[1]
                    print('\tClient request ', request_file)
                    myfile = request_file.split('?')[0]
                    myfile = myfile.strip('/')
                    if(myfile == ''):
                        myfile = 'test.html'

                    # 404 ERROR CHECK
                    try:
                        myfile_path = Path(myfile)
                        file = open(myfile)
                        contents = file.read()
                        file.close()

                        # OK 200 / ERROR 304 CHECK
                        if(self.MODIFY_CHECK != myfile_path.stat().st_mtime):
                            self.MODIFY_CHECK = myfile_path.stat().st_mtime
                            response = 'HTTP/1.1 200 OK\n\n' + contents
                        else:
                            response = 'HTTP/1.1 304 NOT MODIFIED\n\n' + contents
                        
                    except FileNotFoundError:
                        response = 'HTTP/1.1 404 NOT FOUND\n\n File Not Found'
                else: # 'GET' not fount
                    response = 'HTTP/1.1 400 BAD REQUEST\n\n'
                
            print("\n\tPrinting server response: ")
            print(response)

            # Closing sock
            self.client_sock.sendall(response.encode())
            self.client_sock.close()

def main():
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    print('Server is binded to port %s ...' % PORT)

    while True:
        try:
            server.listen(1)
            print('Server is listening...')
            clock_time = time.time()
            client_sock, client_addr = server.accept()
            newthread = ClientThread(client_addr, client_sock, clock_time)
            newthread.start()
        except KeyboardInterrupt:
            print('\n*****\tSERVER PROCESS TERMINATED\t*****')
            break

if __name__ == '__main__':
    main()
