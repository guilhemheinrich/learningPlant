import dataTransformation
import sklearn
import numpy as np

filepath = "data\\allPlants.csv"

datahandle = dataTransformation.dataHandler() 
datahandle.addRawData(filepath)
transformed_data = datahandle.buildDatum() 
asArray_data = dataTransformation.transformDatumIntoArray(transformed_data)

npArray = np.array(asArray_data)

print(npArray)