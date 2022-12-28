# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 16:16:11 2022

@author: Alexander
"""
import json
import numpy as np
from rdp import rdp

def chaikins_corner_cutting(coords, refinements=5):
    coords = np.array(coords)

    for _ in range(refinements):
        L = coords.repeat(2, axis=0)
        R = np.empty_like(L)
        R[0] = L[0]
        R[2::2] = L[1:-1:2]
        R[1:-1:2] = L[2::2]
        R[-1] = L[-1]
        coords = L * 0.75 + R * 0.25
    
    return coords

with open("test.geojson") as f:
  features = json.load(f)["features"]

coords = features[0]["geometry"]["coordinates"][0]
#start = coords[0]
#coords = coords[1:-1]
newCoords = rdp(coords, epsilon=0.00015)
newCoords = chaikins_corner_cutting(newCoords)
#prev_coord = start
#for i in coords:
#    newCoords.append([(prev_coord[0]+i[0])/2, (prev_coord[1]+i[1])/2])
#    prev_coord = i
#newCoords.insert(0, newCoords[-1])
#newCoords.append(start)
print(newCoords.tolist())

x={
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          newCoords.tolist()
        ],
        "type": "Polygon"
      }
    }
  ]
}
with open('data.json', 'w') as f:
    json.dump(x, f)
