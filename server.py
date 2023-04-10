import socketserver 
import database
import json
import hashlib
import base64



class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        recevied_data = self.request.recv(2048)
        data = recevied_data




if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()