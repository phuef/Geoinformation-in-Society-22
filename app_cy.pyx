# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:33:03 2022

@author: Alexander Pilz
"""
from flask import Flask, jsonify
from ast import literal_eval
import json

#configure flask to use HTTP 1.1 only
from werkzeug.serving import WSGIRequestHandler
from werkzeug.serving import BaseWSGIServer
WSGIRequestHandler.protocol_version = "HTTP/1.1"
BaseWSGIServer.protocol_version = "HTTP/1.1"

from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import uuid

from osgeo import osr, ogr


class DistanceStack:
    def __init__(self, path):
        raster = gdal.Open(path, 0)
        self.uuid = str(uuid.uuid4())
        self.raster = raster
        self.bands = []
        for i in range(1, raster.RasterCount + 1):
            band = raster.GetRasterBand(i)
            self.bands.append(band)
            self.bands[i-1].ComputeStatistics(0)
        
        
        self.transform = raster.GetGeoTransform()
        self.projection = raster.GetProjection()
        self.srs = osr.SpatialReference(wkt=self.projection)
        raster = band = None
        
    '''
    *
    *
    *
    *
    '''
    def distanceStackInfo(self):
        print("==> Projection: ", self.raster.GetProjection())  # get projection
        print("==> Columns:", self.raster.RasterXSize)  # number of columns
        print("==> Rows:", self.raster.RasterYSize)  # number of rows
        print("==> Band count:", self.raster.RasterCount)  # number of bands
        
    '''
    *
    *
    *
    *
    '''
    def distanceBandInfo(self, band):
        print("==> Minimum:", self.bands[band].GetMinimum())
        print("==> Maximum:", self.bands[band].GetMaximum())
        print("==> NoData value:", self.bands[band].GetNoDataValue())
        
    '''
    *
    *
    *
    *
    '''
    def filterStack(self, filterValues):
        filteredArrays = [] 
        
        cdef int i
        for i in range(0, len(filterValues)):
            array = self.bands[filterValues[i][0]].ReadAsArray()

            filteredArray = array <= filterValues[i][1]/10
            
            filteredArrays.append(filteredArray)
            
        combinedArray = filteredArrays[0]
        
        cdef int y
        for y in filteredArrays:
            combinedArray *= y
            
        driver = gdal.GetDriverByName('MEM')
        output = driver.Create('', xsize=self.raster.RasterXSize, ysize=self.raster.RasterYSize, bands=1, eType=gdal.GDT_Byte)
        output.SetGeoTransform(self.transform) #set geotransform of output image
        output.SetProjection(self.projection)
        output.GetRasterBand(1).WriteArray(combinedArray.astype(int))  # write the array to the raster
        output.GetRasterBand(1).SetNoDataValue(-999)  # set the no data value
        
        drv = ogr.GetDriverByName('GEOJSON')
        outfile = drv.CreateDataSource("./data/results/" + self.uuid + ".json") 
        outlayer = outfile.CreateLayer('test', srs = self.srs)
        newField = ogr.FieldDefn('DN', ogr.OFTReal)
        outlayer.CreateField(newField)
        
        gdal.Polygonize(output.GetRasterBand(1), None, outlayer, 0, [])
        output = outfile = outlayer =  None 
        return self.uuid

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
    params = literal_eval(requestParams) #parse parameters
    fileID = stack.filterStack(params) #filter stack
    
    payload = json.load(open('./data/results/' + fileID + '.json')) #load results
    return payload, 200 #return results

#run application
if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False) #start app
