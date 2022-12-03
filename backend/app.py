# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:33:03 2022

@author: Alexander Pilz
"""
#Imports of required packages, classes and functions
from flask import Flask
from flask_cors import CORS
from ast import literal_eval
import json
from geojson_rewind import rewind
from utils_cy import DistanceStack #import "cythonized" utils
#from utils import DistanceStack

#configure flask to use HTTP 1.1 only
from werkzeug.serving import WSGIRequestHandler
from werkzeug.serving import BaseWSGIServer
WSGIRequestHandler.protocol_version = "HTTP/1.1"
BaseWSGIServer.protocol_version = "HTTP/1.1"

#define app
app = Flask(__name__)
CORS(app) #allow cross-origin-requests

'''
* Title: Hello-World Route 
* Description: A route which is accessible
* via localhost:5050/ and returns a Hello World! with a the HTTP-Statuscode 200 
'''
@app.route("/", methods = ['GET'])
def helloWorld():
    return "Hello World!", 200

'''
* Title: 
* Description:
'''
@app.route('/request/<requestParams>', methods = ['GET'])
def request(requestParams):
    stack = DistanceStack() #create stack
    #stack.distanceStackInfo()
    params = literal_eval(requestParams) #parse parameters
    fileID = stack.filterStack(params) #filter stack
    
    geojson = json.load(open('usr/src/backend/results/' + fileID + '.json')) #load results
    geojsonRewound = rewind(geojson)
    return geojsonRewound, 200 #return results

#run application
if __name__ == '__main__':
    '''
    * Port: 5050
    '''
    app.run(port=5050, debug=True, use_reloader=False, host='0.0.0.0') #start app