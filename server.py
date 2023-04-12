import socketserver 
import database
import json
import hashlib
import base64
from flask import Flask
from flask_sock import Sock



class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        received_data = self.request.recv(2048)
        header = received_data[ :received_data.find(b'\r\n\r\n')]
        request = header.split(b'\r\n')

        if b'GET / ' in request[0]:
            with open("frontend/index.html","rb") as html_file: 
                bytearray = html_file.read()
                file_length = len(bytearray)
                self.request.sendall((f"HTTP/1.1 200 OK\r\nContent-Length: "+str(file_length)+"\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\n\r\n").encode()+bytearray)
                

        elif b'/loading.js' in request[0]:
            with open("frontend/loading.js", "rb") as js_file:
                bytearray = js_file.read()
                file_length = len(bytearray)
                self.request.sendall((f"HTTP/1.1 200 OK\r\nContent-Length:"+str(file_length)+"\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/javascript; charset=utf-8\r\n\r\n").encode()+bytearray)
        elif b'/main.js' in request[0]:
            with open("frontend/main.js", "rb") as css_file:
                bytearray = css_file.read()
                file_length = len(bytearray)
                self.request.sendall((f"HTTP/1.1 200 OK\r\nContent-Length:"+str(file_length)+"\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/css; charset=utf-8\r\n\r\n").encode()+bytearray)
        elif b'/script.js' in request[0]:
            with open("frontend/script.js", "rb") as css_file:
                bytearray = css_file.read()
                file_length = len(bytearray)
                self.request.sendall((f"HTTP/1.1 200 OK\r\nContent-Length:"+str(file_length)+"\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/css; charset=utf-8\r\n\r\n").encode()+bytearray)
        elif b'/items.js' in request[0]:
            with open("frontend/items.js", "rb") as css_file:
                bytearray = css_file.read()
                file_length = len(bytearray)
                self.request.sendall((f"HTTP/1.1 200 OK\r\nContent-Length:"+str(file_length)+"\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/css; charset=utf-8\r\n\r\n").encode()+bytearray)
        elif b'/styleguide.js' in request[0]:
            with open("frontend/styleguide.js", "rb") as css_file:
                bytearray = css_file.read()
                file_length = len(bytearray)
                self.request.sendall((f"HTTP/1.1 200 OK\r\nContent-Length:"+str(file_length)+"\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/css; charset=utf-8\r\n\r\n").encode()+bytearray)                                
        elif b'/style.css' in request[0]:
            with open("frontend/style.css", "rb") as css_file:
                bytearray = css_file.read()
                file_length = len(bytearray)
                self.request.sendall((f"HTTP/1.1 200 OK\r\nContent-Length:"+str(file_length)+"\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/css; charset=utf-8\r\n\r\n").encode()+bytearray)
        
        else:
           self.request.sendall("HTTP/1.1 404 Not Found\r\nContent-Length: 5\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nError".encode())
    


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 6000

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()