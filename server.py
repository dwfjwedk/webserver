
#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import subprocess
from io import BytesIO

from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np
from urllib import request, parse

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(b'Hello, world!')
        # Send message back to client
        message = "<font size=+3>Hello world!(HTML)</font><p>"
        self.wfile.write(bytes(message, "utf8"))

  def do_POST(self):
        content_length = int(self.headers['Content-Length']) #  Gets the size of data
        body = self.rfile.read(content_length)  # - Gets the data itself
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'wto proishodit????. ')
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

def run():
  print('starting server...')

  # Server settings
  # Choose port 8081, for port 80, which is normally used for a http server, you need root access
  server_address = ('', 8888)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

class modelnn(object):
    """docstring"""

  def __init__(self,data):
        """Constructor"""
        self.data = data

  def get_result(self):
        train = pd.DataFrame([[0, 0, 1, 0],[1, 1, 1, 1], [1, 0, 1, 1], [0, 1, 1,0]])
        train.columns = ['ohe1', 'ohe2','ohe3', 'output']
        X_train = train[['ohe1', 'ohe2','ohe3']]
        y_train = train['output']

        batch_size = 2
        epochs = 6
        model = Sequential()
        model.add(Dense(3, activation = 'relu', input_shape=(3,)))  
        model.add(Dense(1, activation = 'sigmoid'))  
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, verbose=0); 

        a = model.predict(self.data)
        b =np.apply_along_axis(lambda x: round(x[0]), 1, a )
        return b


X_test = pd.DataFrame([[0, 0, 1],[1, 1, 1], [1, 0, 1], [0, 1, 1],[1, 0, 0]])
X_test.columns = ['ohe1', 'ohe2','ohe3']
resultat = modelnn(X_test)
b = resultat.get_result() 


run()
