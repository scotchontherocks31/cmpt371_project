from socket import *
import threading
import os
from _thread import *

HOST = gethostbyname("localhost")
PORT = 8080
CWD = os.getcwd()
PRINT_LOCK = threading.Lock()

class ClientThread(threading.Thread):
    def __init__(self, client_addr, client_sock):
        threading.Thread.__init__(self)
        self.client_sock = client_sock
        self.client_addr = client_addr
        print("\nNew connection added at: ", client_addr)

    def run(self):
        print("\nConnection from: ", self.client_addr)

        while True:
            # request may need further debugging
            try:
                request = self.client_sock.recv(1024).decode()
                print("\nProducing request: ")
                print(request)
            except OSError:
                break

            # Get content of test.html
            try:
                file = open('test.html')  # might need to modify
                content = file.read()
                file.close()

                response = 'HTTP/1.1 200 OK\n\n' + content

            except FileNotFoundError:  # 404 Error
                response = 'HTTP/1.1 404 NOT FOUND\n\n File Not Found'

            except TimeoutError:  # if cannot connect
                response = 'HTTP/1.1 408 REQUEST TIME OUT\n\n Request Timed Out'

            except KeyboardInterrupt:
                self.client_sock.close()
                print("\nKEYBOARD INTERRUPT: Shutting down server per users request.")

            #TODO: 304 Not Modified

            #TODO: 400 Bad request

            self.client_sock.sendall(response.encode())
            self.client_sock.close()

def main():

    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    print('Server is binded to port %s ...' % PORT)

    while True:
        server.listen(1)
        print('Server is listening...')
        client_sock, client_addr = server.accept()
        newthread = ClientThread(client_addr, client_sock)
        newthread.start()
    return

if __name__ == '__main__':
    main()
