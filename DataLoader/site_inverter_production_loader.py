#import psycopg2
import json
#import psycopg2.extras
#from config import config
#import os
from DataLoader.DataLoader import DataLoader

class SiteInverterProductionLoader(DataLoader):
	"""docstring for SiteInverterProductionLoader"""
	def __init__(self, file_list=None, folder_path=None):
		super(SiteInverterProductionLoader, self).__init__(table_name='site_inverter_production',
			column_names=['value','date','equipment_id','data_source','unit'],
			#file_list=file_list,
			folder_path=folder_path
			)
		
		self.path = '123'
		

	def get_data(self, file_path):
	    
	    data = None
	    
	    try:
	    
	        with open(file_path) as json_file:
	    
	            data = json.load(json_file)         
	    
	    except Exception as e:
	    	
	    	print('unable to load data from file ',file_path)
	        
	    return data

	def make_SE_production_dict(self, data):
	    
	    d = []
	    
	    if not data or not data['sitesEnergy']:
	    	
	    	print('data set is empty')
	    	
	    	return d

	    timeUnit = data['sitesEnergy'].get('timeUnit',None)
	    
	    #unit = data['sitesEnergy'].get('unit',None)
	    unit = 'kWh'
	    
	    for site in data['sitesEnergy']['siteEnergyList']:
	        #print(type(site))
	        site_id = site.get('siteId',None)        #measuredBy = site['energyValues']['measuredBy']

	        for val in site['energyValues']['values']:

	        	v = None
	        
	        	if val['value']:
	        	
	        		v = val['value']/1000

	        	date = val.get('date',None)

	        	di = {'date':date, 'value':v ,'equipment_id':site_id,'data_source':'SolarEdge','unit':unit}

	        	d.append(di)

	    return d

	def load_file_to_db(self, file_path, conn):
	    
	    #file_path = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\SolarEdge\site_production\bulk_energy_2019-01-01.json'
	    
	    data = self.get_data(file_path)
	    
	    columns = ['value','date','equipment_id','data_source','unit']
	    
	    table_name = 'site_inverter_production'
	    
	    s = self.make_sql_string(self.table_name, self.columns)
	    
	    list_of_dict = self.make_SE_production_dict(data)
	    
	    self.sql_query(conn,s,list_of_dict)  

	    return s
