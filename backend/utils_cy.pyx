# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 16:08:13 2022

@author: Alexander Pilz
"""
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import uuid

from osgeo import osr, ogr
from werkzeug.routing import BaseConverter

'''
*
*
*
*
'''
class DistanceStack:
    def __init__(self, path):
        raster = gdal.Open(path, 0)
        self.uuid = str(uuid.uuid4())
        self.raster = raster
        self.bands = []

        cdef int i
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
        
        cdef int y
        for y in range(0, len(filterValues)):
            array = self.bands[filterValues[y][0]].ReadAsArray()

            filteredArray = array <= filterValues[y][1]/10
            
            filteredArrays.append(filteredArray)
            
        combinedArray = filteredArrays[0]
        
        cdef int x
        for x in range(0, len(filteredArrays)):
            combinedArray *= filteredArrays[x]
            
        driver = gdal.GetDriverByName('MEM')
        output = driver.Create('', xsize=self.raster.RasterXSize, ysize=self.raster.RasterYSize, bands=1, eType=gdal.GDT_Byte)
        output.SetGeoTransform(self.transform) #set geotransform of output image
        output.SetProjection(self.projection)
        output.GetRasterBand(1).WriteArray(combinedArray.astype(int))  # write the array to the raster
        output.GetRasterBand(1).SetNoDataValue(-999)  # set the no data value
        
        drv = ogr.GetDriverByName('GEOJSON')
        outfile = drv.CreateDataSource("./results/" + self.uuid + ".json") 
        outlayer = outfile.CreateLayer('test', srs = self.srs)
        newField = ogr.FieldDefn('DN', ogr.OFTReal)
        outlayer.CreateField(newField)
        
        gdal.Polygonize(output.GetRasterBand(1), None, outlayer, 0, [])
        output = outfile = outlayer =  None 
        return self.uuid

