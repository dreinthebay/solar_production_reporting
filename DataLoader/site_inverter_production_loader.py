import psycopg2
import json
import psycopg2.extras
from config import config
import os

def get_connection():
    
    params = connect_to_postgres()

    conn = psycopg2.connect(**params)

    return conn

def connect_to_postgres(cloud_connect=True):
    
    print('testing cloud connect = ', cloud_connect)
    
    if cloud_connect:

        print('Connection type: Cloud')

        return config(section='postgresql')

    else:

        print('Connection type: Localhost')

        return config(section='localhost')

def get_data(file_path):
    
    data = None
    
    try:
    
        with open(file_path) as json_file:
    
            data = json.load(json_file)         
    
    except Exception as e:
    	
    	print('unable to load data from file ',file_path)
        
        #raise e

    return data

def make_sql_string(table_name,list_of_column_names):
    
    column_values = ','.join(list_of_column_names)
    
    values = ','.join(['%('+str(x)+')s' for x in list_of_column_names])
    
    s = """INSERT INTO {table_name} ({column_values}) VALUES ({values})""".format(
    table_name=table_name,
    column_values=column_values,
    values=values
    )
    
    #s = """INSERT INTO {table_name} VALUES ({values})""".format(table_name=table_name,column_values=column_values,values=values)
    
    print(s)
    
    return s

def make_SE_production_dict(data):
    
    d = []
    
    if not data or not data['sitesEnergy']:
    	
    	print('data set is empty')
    	
    	return d

    timeUnit = data['sitesEnergy'].get('timeUnit',None)
    
    unit = data['sitesEnergy'].get('unit',None)
    
    for site in data['sitesEnergy']['siteEnergyList']:
        #print(type(site))
        site_id = site.get('siteId',None)        #measuredBy = site['energyValues']['measuredBy']

        for val in site['energyValues']['values']:
        
            di = {**val,'equipment_id':site_id,'data_source':'SolarEdge','unit':unit}
        
            d.append(di)

    return d

def sql_query(conn,sql_string,list_of_dict):
    
    with conn.cursor() as cursor:
    
        iter_data = (d for d in list_of_dict)
    
        print(type(iter_data))
    
        psycopg2.extras.execute_batch(
    
            cursor,
    
            sql_string,
    
            iter_data
        )
    
    conn.commit()

    return 1

def close_connection(conn):
	
	conn.close()
	
	pass

def load_file_to_db(file_path, conn):
    
    #file_path = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\SolarEdge\site_production\bulk_energy_2019-01-01.json'
    
    data = get_data(file_path)
    
    columns = ['value','date','equipment_id','data_source','unit']
    
    table_name = 'site_inverter_production'
    
    s = make_sql_string(table_name,columns)
    
    list_of_dict = make_SE_production_dict(data)
    
    sql_query(conn,s,list_of_dict)  

    return s

def load_single_file(file_path):
	
	conn = get_connection()
	
	load_file_to_db(file_path, conn)
	
	close_connection(conn)

def load_files_to_db(file_list=None, folder=None):
	# if file list passed
	if file_list:
	
		conn = get_connection()
	
		for file in file_list:
	
			load_file_to_db(file, conn)
		
		close_connection(conn)

	elif folder:
	
		conn = get_connection()

		#folder = file_path = os.path.join(self.app_folder, 'raw_data', self.company_name, self.equipment_company_name, sub_directory, file_name)

		for file in os.listdir(folder):

			file_path = folder + os.sep + file

			print(file_path)
	
			load_file_to_db(file_path, conn)
	
		close_connection(conn)
	
	else:
	
		print('incorrect parameters passed')

	return 1


