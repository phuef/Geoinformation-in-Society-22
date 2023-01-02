# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:33:03 2022

@author: Alexander Pilz
"""
#Imports of required packages, classes and functions
from flask import Flask, request, make_response, render_template, jsonify
from flask_cors import CORS
from ast import literal_eval
import json
from utils_cy import DistanceStack #import "cythonized" utils
#from utils import DistanceStack
import traceback

#configure flask to use HTTP 1.1 only
from werkzeug.serving import WSGIRequestHandler
from werkzeug.serving import BaseWSGIServer
WSGIRequestHandler.protocol_version = "HTTP/1.1"
BaseWSGIServer.protocol_version = "HTTP/1.1"

#define app
app = Flask(__name__)
#allow cross-origin-requests from all origins
CORS(app, supports_credentials=True, resources={r"/request/*": {"origins": "*"}}) 

'''
* Title: Hello-World Route 
* Description: A route which is accessible
*              via localhost:5050/ and returns a Hello World! with a the HTTP-Statuscode 200 
'''
@app.route("/", methods = ['GET'])
def helloWorld():
    return "Hello World!", 200

'''
* Title: Coffee Route 
* Description: A route which is accessible
*              via localhost:5050/brewCoffee and returns HTTP-Statuscode 418
'''
@app.route("/brewCoffee", methods = ['GET'])
def tea():
    return "The server refuses to brew coffee because it is, permanently, a teapot.", 418

'''
* Title: API-Description Route 
* Description: A route which is accessible
*              via localhost:5050/apiDescription and returns OpenAPI Documentation of the API
'''
@app.route("/apiDescription", methods = ['GET'])
def api():
    try:
        if(request.args.get('f')=="text/html" or request.args.get('f') == None): 
            response = render_template('open_api_doc.html') 
            return response, 200
        elif(request.args.get('f')=="application/json"):
            file = open('usr/src/backend/data/open_api_doc.json',) 
            payload = json.load(file) 
            file.close() 
            response = jsonify(payload) 
            return response, 200
        else:
            return "HTTP status code 406: not acceptable", 406 
    except(Exception):
        print(traceback.format_exc())
        return "Internal Server Error", 500

'''
* Title: 
* Description: (band, min, max)
'''
@app.route('/request/<requestParams>', methods = ['GET', 'OPTIONS'])
def raster(requestParams):
    #try:
    if(request.method == 'GET'): #actual request using GET
        stack = DistanceStack() #create stack
        #stack.distanceStackInfo()
        params = literal_eval(requestParams) #parse parameters
        for i in params:
            if(i[1] != None and i[2] != None):
                if(i[1] > i[2]):
                    return "Bad Request", 400
            elif(i[1] == None and i[2] == None):
                return "Bad Request", 400
        stack.filterStack(params) #filter stack
        geojson = stack.filterResult() #load and filter results
        
        response = make_response(geojson) #generate response
        #add headers
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        response.headers.add("Referrer-Policy", 'no-referrer')
        
        return response, 200 #return results
    elif(request.method == 'OPTIONS'): #preflight request using OPTIONS
        response = make_response() #generate response
        #add headers
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        response.headers.add("Referrer-Policy", 'no-referrer')
        return response, 204 #return preflight response
    #except Exception:
        print(traceback.format_exc())
        return "Internal Server Error", 500

#run application
if __name__ == '__main__':
    '''
    * Port: 5050
    '''
    app.run(port=5050, debug=True, use_reloader=False, host='0.0.0.0') #start app
    #Request localhost:5050/request/[(0,300,None)]