
#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
import json
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "<font size=+3>Hello world!</font><p>"
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        body = self.rfile.read(content_length)  
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request.\n')
        response.write(b'Received as a test data: ')
        response.write(body)        
        response.write(b'\nPredicted by nn model:')
        X_test = pd.DataFrame(json.loads(body.decode('utf-8')).values())        
        resultat = modelnn(X_test)

        b = resultat.get_result()
        response.write(str(b).encode('UTF-8'))
        self.wfile.write(response.getvalue())

def run():
    print('starting server...')
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

class modelnn(object):

    def __init__(self,data):
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

run()
