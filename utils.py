# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 16:08:13 2022

@author: Alexander Pilz
"""
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import uuid

from osgeo import osr

class DistanceStack:
    def __init__(self, path):
        raster = gdal.Open(path)
        self.uuid = str(uuid.uuid4())
        self.raster = raster
        self.bands = []
        for i in range(1, raster.RasterCount + 1):
            band = raster.GetRasterBand(i)
            self.bands.append(band)
            self.bands[i-1].ComputeStatistics(0)
        raster = band = None
        
        raster = None
    
    def distanceStackInfo(self):
        print("==> Projection: ", self.raster.GetProjection())  # get projection
        print("==> Columns:", self.raster.RasterXSize)  # number of columns
        print("==> Rows:", self.raster.RasterYSize)  # number of rows
        print("==> Band count:", self.raster.RasterCount)  # number of bands
        
    def getBandValues(self, band):
        print("==> Minimum:", self.bands[band].GetMinimum())
        print("==> Maximum:", self.bands[band].GetMaximum())
        print("==> NoData value:", self.bands[band].GetNoDataValue())
        
    def filterStack(self, filterValues):
        array = self.bands[filterValues[0][0]].ReadAsArray()
        
        filteredArray = array <= filterValues[0][1]
        
        filteredArrayInt = filteredArray.astype(int)

        driver = gdal.GetDriverByName('GTiff')
        output = driver.Create("./data/" + self.uuid + '.tiff', xsize=self.raster.RasterXSize, ysize=self.raster.RasterYSize, bands=1, eType=gdal.GDT_Byte)
        

        crs = osr.SpatialReference()
        crs.ImportFromEPSG(3857)
        output.SetProjection(crs.ExportToWkt())
        output.GetRasterBand(1).WriteArray(filteredArrayInt)  # write the array to the raster
        output.GetRasterBand(1).SetNoDataValue(-999)  # set the no data value
        output = None 

        

stack = DistanceStack('./data/distanceTheater10x10.tif')
#stack.distanceStackInfo()
#stack.getBandValues(0)
stack.filterStack([(0, 1000)])

