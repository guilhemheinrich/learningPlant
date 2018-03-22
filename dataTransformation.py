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
                # print(line)
                hash_key = hashlib.md5()
                hash_key.update(line['genotype'])
                hash_key.update(line['experience'])
                hash_key.update(line['replicate'])
                key = hash_key.hexdigest()
                if key not in self.data:
                    self.data[key] = {}
                if 'data' not in self.data[key]:
                    self.data[key]['data'] = []
                if 'informations' not in self.data[key]:
                    self.data[key]['informations'] = {
                        'genotype' : line['genotype'],
                        'experience' : line['experience'],
                        'replicate' : line['replicate']
                    }
                hash_key.update(str(line['estimatedLeafArea..LA.']))
                leaf_area = {
                        'key' : hash_key.hexdigest(),
                        'value' : line['estimatedLeafArea..LA.'],
                }
                hash_key.update(str(line['estimatedBiomass..B.']))
                biomass = {
                        'key' : hash_key.hexdigest(),
                        'value' : line['estimatedBiomass..B.'],
                }
                date = time.strptime(line['date'], '%Y-%m-%d %H:%M:%S')
                date = time.mktime(date)
                variables = {
                    'leafArea' : leaf_area,
                    'biomass' : biomass
                }
                datum = {'x' : date, 'variables' : variables }
                self.data[key]['data'].append(datum)
    def processPlantDatum(self, plant, variable_name):   
        out_allDatum = {}
        data_length = len(plant['data'])
        for index_datum in range(data_length):
            datum = {}
            datum['x'] = plant['data'][index_datum]['x']
            datum[variable_name] = plant['data'][index_datum]['variables'][variable_name]['value']
            if (index_datum > 1):
                datum['x-1'] = plant['data'][index_datum - 1]['x']
                datum[variable_name + '-1'] = plant['data'][index_datum - 1]['variables'][variable_name]['value']
                datum['-1'] = datum['x'] - datum['x-1']
            else:
                datum['x-1'] = None
                datum[variable_name + '-1'] = None
                datum['-1'] = None
            if (index_datum > 2):
                datum['x-2'] = plant['data'][index_datum - 2]['x']
                datum[variable_name + '-2'] = plant['data'][index_datum - 2]['variables'][variable_name]['value']
                datum['-2'] = datum['x'] - datum['x-2']
            else:
                datum['x-2'] = None
                datum[variable_name + '-2'] = None
                datum['-2'] = None
            if (index_datum + 1 < data_length - 1):
                datum['x+1'] = plant['data'][index_datum + 1]['x']
                datum[variable_name + '+1'] = plant['data'][index_datum + 1]['variables'][variable_name]['value']
                datum['+1'] = datum['x'] - datum['x+1']
            else:
                datum['x+1'] = None
                datum[variable_name + '+1'] = None
                datum['+1'] = None
            if (index_datum + 2 < data_length - 1):
                datum['x+2'] = plant['data'][index_datum + 2]['x']
                datum[variable_name + '+2'] = plant['data'][index_datum + 2]['variables'][variable_name]['value']
                datum['+2'] = datum['x'] - datum['x+2']
            else:
                datum['x+2'] = None
                datum[variable_name + '+2'] = None
                datum['+2'] = None
            key = plant['data'][index_datum]['variables'][variable_name]['key']
            out_allDatum[key] = datum
        print(out_allDatum)
        return out_allDatum
    def buildDatum(self):
        transformed_data = []
        for plant_key in self.data:
            plant = self.data[plant_key]
            plant['data'] = sorted(plant['data'], key=lambda k: k.get('x', 0), reverse=False)
        for plant_key in self.data:
            plant = self.data[plant_key]
            transformed_data.append(self.processPlantDatum(plant, 'leafArea'))
        return transformed_data
                    

filepath = "data\\allPlants.csv"

datahandle = dataHandler() 
datahandle.addRawData(filepath)
datahandle.buildDatum() 
print(datahandle.buildDatum()[0])






