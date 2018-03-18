# Importer dans un tableau, ID = genotype X replicate X experiment

import csv
import datetime
import hashlib
import time


class dataHandler:
    
    def __init__(self):
        self.data = {}
    def addRawData(self, filepath):
        with open(filepath) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for line in reader:
                print(line)
                key = hashlib.md5()
                key.update(line['genotype'])
                key.update(line['experience'])
                key.update(line['replicate'])
                key = key.hexdigest()
                # key.digest()
                # print(key.hexdigest())
                date = time.strptime(line['date'], '%Y-%m-%d %H:%M:%S')
                value = {
                    'leafArea' : line['estimatedLeafArea..LA.'],
                    'biomass' : line['estimatedBiomass..B.']
                }
                datum = {'x' : date, 'value' : value }
                if key not in self.data:
                    self.data[key] = {}
                if 'data' not in self.data[key]:
                    self.data[key]['data'] = []
                self.data[key]['data'].append(datum)
                if 'informations' not in self.data[key]:
                    self.data[key]['informations'] = {
                        'genotype' : line['genotype'],
                        'experience' : line['experience'],
                        'replicate' : line['replicate']
                    }
                
        

filepath = "data\\allPlants.csv"

datahandle = dataHandler()
datahandle.addRawData(filepath)



