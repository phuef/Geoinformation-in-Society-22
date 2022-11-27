# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:33:03 2022

@author: Alexander Pilz
"""
from flask import Flask

from werkzeug.serving import WSGIRequestHandler
from werkzeug.serving import BaseWSGIServer
WSGIRequestHandler.protocol_version = "HTTP/1.1"
BaseWSGIServer.protocol_version = "HTTP/1.1"

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def helloWorld():
    return "Hello World!", 200

@app.route("/request", methods = ['GET'])
def request():
    return "Request", 200

#run application
if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False) 
