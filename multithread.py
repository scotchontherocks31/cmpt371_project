from socket import *
import sys
import threading
import time
import socketserver
import http.server
import os

HOST = gethostname()
PORT = 8080
CWD = os.getcwd()

class SimpleThreadServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass


server = SimpleThreadServer(('', PORT), http.server.SimpleHTTPRequestHandler)
print("Serving HTTP traffic from", CWD, "on", HOST, "using port", PORT)

try:
    while 1:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print("\nShutting down server per users request.")
