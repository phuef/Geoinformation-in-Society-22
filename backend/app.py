# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:33:03 2022

@author: Alexander Pilz
"""
from flask import Flask, jsonify
from ast import literal_eval
import json
from utils_cy import DistanceStack
#from utils import DistanceStack

#configure flask to use HTTP 1.1 only
from werkzeug.serving import WSGIRequestHandler
from werkzeug.serving import BaseWSGIServer
WSGIRequestHandler.protocol_version = "HTTP/1.1"
BaseWSGIServer.protocol_version = "HTTP/1.1"

#define app
app = Flask(__name__)

'''
*
*
*
*
'''
@app.route("/", methods = ['GET'])
def helloWorld():
    return "Hello World!", 200

'''
*
*
*
*
'''
@app.route('/request/<requestParams>', methods = ['GET'])
def request(requestParams):
    stack = DistanceStack('./data/composit10x10.tif') #create stack
    stack.distanceStackInfo()
    params = literal_eval(requestParams) #parse parameters
    fileID = stack.filterStack(params) #filter stack
    
    payload = json.load(open('./results/' + fileID + '.json')) #load results
    return payload, 200 #return results

#run application
if __name__ == '__main__':
    app.run(port=5050, debug=True, use_reloader=False, host='0.0.0.0') #start app
