# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 20:04:12 2020

@author: slin2
"""

import csv
import json

import os

path = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\eGauge\production'

file_name = os.path.join(path,"special_all_egauge_production_from_2020-02-01_to_2020-03-01.json")
with open(file_name) as json_file:
    data = json.load(json_file)	
		
csv_columns = ['site', 'date','generation','units']

data['sites']['0']

l = []


csv_file = os.path.join(path,"special_all_egauge_production_from_2020-02-01_to_2020-03-01.csv")
try:
    with open(csv_file, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns)
        for key, d in data['sites'].items():
                        
            site = d.get('site','no site')
            units = d['data'].get('units','no units')
            
            date = d['data']['values'].get('date','no date')
            gen = d['data']['values'].get('value', 'no value')
            l = [site, date, gen, units]
            print(l)
            #t = ','.join(map(str, l))
            #print(t)
            writer.writerow(l)
            
except IOError:
    print("I/O error")