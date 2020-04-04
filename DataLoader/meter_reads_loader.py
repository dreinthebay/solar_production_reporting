import psycopg2
import psycopg2.extras
from config import config
import os
import xml.etree.ElementTree as ET


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

# deprecate?
def get_data(file_path):
    
    data = None
    
    try:
    
        with open(file_path, 'r') as text:

        	data = text.read()
        
    except Exception as e:
    	
    	print('unable to load data from file ',file_path)
        
        #raise e

    return data

def get_xml_root(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except Exception as e:
        print('empty file:',file_path)
    return None

def parse_meter_read(root):
    headers=[]
    vals=[]
    print('There are ',len(root.findall('data')),' data entries. Expecting 1 or 2')
    if len(root.findall('data')) > 2 or len(root.findall('data')) < 1:
        return headers, vals
    
    data = root.find('data')
    for cname in data.findall('cname'):
        #print(cname.text)
        headers.append(cname.text)
    for d in root.findall('data'):
        for r in d.findall('r'):
            for c in r.findall('c'):
                vals.append(c.text)

    #r = data.find('r')
    #for c in r.findall('c'):
        #print(c.text)
        #vals.append(c.text)
        
    return headers, vals

def make_meter_reads_dict(headers,vals,equipment_id,date):
    list_of_reads = []
    for i in range(len(headers)):
        d = {}
        d['equipment_id'] = equipment_id
        d['date'] = date
        d['header'] = headers[i]
        d['value'] = vals[i]
        list_of_reads.append(d)

    return list_of_reads

def make_sql_string(table_name,list_of_column_names):
    
    column_values = ','.join(list_of_column_names)
    
    values = ','.join(['%('+str(x)+')s' for x in list_of_column_names])
    
    s = """INSERT INTO {table_name} ({column_values}) VALUES ({values})""".format(
    table_name=table_name,
    column_values=column_values,
    values=values
    )
    return s
def close_connection(conn):
    
    conn.close()
    
    pass


def get_equipment_id(file_path):
    return file_path[-9:-4]

def get_date(file_path):
    return file_path[-35:-25]

def load_file_to_db(file_path, conn):
    
    #file_path = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\SolarEdge\site_production\bulk_energy_2019-01-01.json'
    
    root = get_xml_root(file_path)

    if not root: #empty root
        return 0
    
    columns = ['equipment_id','date','header','value']
    
    table_name = 'meter_reads'
    
    s = make_sql_string(table_name,columns)
    date = get_date(file_path)
    equipment_id = get_equipment_id(file_path)

    headers, vals = parse_meter_read(root)
    list_of_reads = make_meter_reads_dict(headers,vals,equipment_id,date)
    
    sql_query(conn,s,list_of_reads)  

    return s
    
def sql_query(conn,sql_string,list_of_dict):
    #print(list_of_dict)
    #print(sql_string)    
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

def single_file_test():
    file_path = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\eGauge\production\2020\04\2020-04-01_meter_read_for_33746.xml'
    file_path = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\eGauge\production\2020\04\2020-04-01_meter_read_for_33044.xml'
    print('starting load')
    load_single_file(file_path)
    print('load complete')

def meter_reads_main():
    folder = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\eGauge\production\2020\04'
    load_files_to_db(folder=folder)

    return 1
# postgres notes
# https://www.psycopg.org/docs/
# https://kb.objectrocket.com/postgresql/insert-json-data-into-postgresql-using-python-part-2-1248
# https://stackoverflow.com/questions/9075349/using-insert-with-a-postgresql-database-using-python
# https://www.psycopg.org/docs/usage.html
# https://stackoverflow.com/questions/29461933/insert-python-dictionary-using-psycopg2
# https://www.forbes.com/sites/adrianbridgwater/2020/03/10/ibm-call-for-code-challenges-software-developers-to-address-climate-change/#661970847330
# https://www.coursera.org/degrees/master-of-applied-data-science-umich?utm_medium=email&utm_source=marketing&utm_campaign=VTFuIGMUEeqd_xFKDENJkw



#    file_path = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\eGauge\production\2020\04\2020-04-01_meter_read_for_33746.xml'
#file_path = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\eGauge\production\2020\04\2020-04-01_meter_read_for_27121.xml'
'''
tree = ET.parse(file_path)
root = tree.getroot()
root.tag

headers = []
vals = []
data = root.find('data')
for cname in data.findall('cname'):
    print(cname.text)
    headers.append(cname.text)
r = data.find('r')
for c in r.findall('c'):
    print(c.text)
    vals.append(c.text)

for child in root:
     print(child.tag, child.attrib)
     for c in child:
         print(c.tag, c.attrib, c.text)
'''
