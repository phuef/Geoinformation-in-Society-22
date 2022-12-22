# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 16:08:13 2022

@author: Alexander Pilz
"""
from osgeo import gdal, ogr
import json
import uuid

'''
* Title: DistanceStack
* Description: The class DistanceStack is the main class with which the distance 
* raster is handled and computation on it are realized
'''
class DistanceStack:
    #Constructor
    def __init__(self):
        raster = gdal.Open('usr/src/backend/data/composit10x10.tif', 0) #open composit distance raster file
        self.uuid = str(uuid.uuid4()) #generate unique identifier
        self.raster = raster #store raster
        self.bands = [] #initialize bands
        for i in range(1, raster.RasterCount + 1): #iterate over bands in raster
            band = raster.GetRasterBand(i) #extract band
            self.bands.append(band)
            self.bands[i-1].ComputeStatistics(0) #compute some key values for each band
        
        
        self.transform = raster.GetGeoTransform() #store transformation
        #self.projection = raster.GetProjection() #store projection
        #self.srs = osr.SpatialReference(wkt=self.projection) #store coordinate reference system
        raster = band = None #free variables
       
    '''
    * Title: distanceStackInfo
    * Description: Outputs some key values of the raster
    '''
    #def distanceStackInfo(self):
    #    print("==> Projection: ", self.raster.GetProjection())  # get projection
    #    print("==> Columns:", self.raster.RasterXSize)  # number of columns
    #    print("==> Rows:", self.raster.RasterYSize)  # number of rows
    #    print("==> Band count:", self.raster.RasterCount)  # number of bands
        
    '''
    * Title: distanceBandInfo
    * Description: Outputs some key values of a band of the raster
    * Parameters: A band number of the underlying raster 
    '''
    #def distanceBandInfo(self, band):
    #    print("==> Minimum:", self.bands[band].GetMinimum())
    #    print("==> Maximum:", self.bands[band].GetMaximum())
    #    print("==> NoData value:", self.bands[band].GetNoDataValue())
        
    '''
    * Title: filterStack
    * Description: Filters the composit distance raster based on given parameters
    * Parameters: The function expects an array with tuples of the form (band, distance in meters)
    * Example parameters: [(0,1000),(1,2000)]
    * Output: The function outputs a GEOJSON containing polygons where the DN value denotes which ares correspond to the
    * parameters and which do not
    '''
    def filterStack(self, filterValues):
        srs = ogr.osr.SpatialReference()
        srs.ImportFromEPSG(4326)   
        filteredArrays = [] #initialize list for filtered bands
        for i in range(0, len(filterValues)): #iterate over filter values
            if(filterValues[i][1] == None):
                array = self.bands[filterValues[i][0]].ReadAsArray() #read corresponding band from raster
                filteredArray = array <= filterValues[i][2]/10 #filter band
                filteredArrays.append(filteredArray) #add filtered array to list
            elif(filterValues[i][2] == None):
                array = self.bands[filterValues[i][0]].ReadAsArray() #read corresponding band from raster
                filteredArray = array >= filterValues[i][1]/10 #filter band
                filteredArrays.append(filteredArray) #add filtered array to list                           
            else:
                array = self.bands[filterValues[i][0]].ReadAsArray() #read corresponding band from raster
                filteredArrayA = array <= filterValues[i][2]/10
                filteredArrayB = array >= filterValues[i][1]/10 #filter band
                filteredArrays.append(filteredArrayA) #add filtered array to list
                filteredArrays.append(filteredArrayB) #add filtered array to list

        combinedArray = filteredArrays[0] #initialize combined array
        
        for y in filteredArrays[1:]: #iterate over filtered bands
            combinedArray *= y #combine boolean values
            
        driver = gdal.GetDriverByName('MEM') #initialize in memory driver
        output = driver.Create('', xsize=self.raster.RasterXSize, ysize=self.raster.RasterYSize, bands=1, eType=gdal.GDT_Byte) #create rater
        output.SetGeoTransform(self.transform) #set geotransform of output image
        output.SetProjection(srs.ExportToWkt()) #set projection of output image
        output.GetRasterBand(1).WriteArray(combinedArray.astype(int))  #write the array to the raster
        output.GetRasterBand(1).SetNoDataValue(-999)  #set the no data value
        
        drv = ogr.GetDriverByName('GEOJSON') #initialize GEOJSON driver
        outfile = drv.CreateDataSource("usr/src/backend/results/" + self.uuid + ".json") #create GEOJSON
        outlayer = outfile.CreateLayer('test', srs=srs, geom_type=ogr.wkbPolygon) #add layer to GEOJSON
        newField = ogr.FieldDefn('DN', ogr.OFTInteger) #create field
        outlayer.CreateField(newField) #add field to GEOJSON
        
        gdal.Polygonize(output.GetRasterBand(1), None, outlayer, 0, []) #polygonize combined raster based on pixel values
        output = outfile = outlayer =  None #free variables
        return self.uuid #return uuid of DistanceStack
    
    def filterResult(self):
        with open('usr/src/backend/results/' + self.uuid + '.json') as f:
            data = json.load(f)
        for feature in data['features']:
            if(feature['properties']['DN'] != 1):
                data['features'].remove(feature)
            feature['geometry']['coordinates'] = feature['geometry']['coordinates'][::-1]
        data['crs'] = "WGS-84 - EPSG: 4326"
        return data