#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        method = self.data.decode('utf-8').splitlines()[0].split()[0]
        path = self.data.decode('utf-8').splitlines()[0].split()[1]
        file_path = './www' + path 
        
        if path.endswith('/'):
            file_path = file_path + 'index.html'

        if method != 'GET':  
            response = 'HTTP/1.1 405 Method Not Allowed\r\nConnection: close\r\n'
        elif os.path.isdir(file_path) and not path.endswith('/'):
            response = 'HTTP/1.1 301 Moved Permanently\r\nLocation: {}\r\n'.format(path)
        elif os.path.isfile(file_path):
            mime_type = self.get_mime_type(file_path)
            if mime_type != None:
                content = self.get_file_content(file_path)
                if content != 'I/OError':
                    response = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\n{}\r\n'.format(mime_type, content)
                else:
                    response = 'HTTP/1.1 404 Not Found\r\nConnection: close\r\n'
            else:
                response = 'HTTP/1.1 404 Not Found\r\nConnection: close\r\n'
        else:
            response = 'HTTP/1.1 404 Not Found\r\nConnection: close\r\n'

        self.request.sendall(bytearray(response,'utf-8'))

    def get_mime_type(self, path):
        mime_type = os.path.splitext(path)[1]
        if mime_type == '.html':
            return 'text/html'
        elif mime_type == '.css':
            return 'text/css'
        else:
            return None

    def get_file_content(self, path):
        try:
            file_ = open(path, 'r')
            content = file_.read()
            file_.close()
            return content
        except Exception:
            content = 'I/OError'

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
