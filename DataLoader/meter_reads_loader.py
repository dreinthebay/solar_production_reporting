#from config import config
import os
import xml.etree.ElementTree as ET
from DataLoader.DataLoader import DataLoader

class MeterReadsLoader(DataLoader):
    """docstring for MeterReadsLoader"""
    def __init__(self,folder_path):
        super(MeterReadsLoader, self).__init__(table_name='meter_reads'
            ,column_names=['equipment_id','date','header','value']
            ,folder_path=folder_path)
        #self.table_name = 'meter_reads'
        #self.columns = ['equipment_id','date','header','value']

    def get_xml_root(self, file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            return root
        except Exception as e:
            print('empty file:',file_path)
        return None

    def parse_meter_read(self, root):
        headers=[]
        vals=[]
        print('There are ',len(root.findall('data')),' data entries. Expecting 1 or 2')
        if len(root.findall('data')) > 2 or len(root.findall('data')) < 1:
            return headers, vals
        
        data = root.find('data')
        for cname in data.findall('cname'):
            headers.append(cname.text)
        for d in root.findall('data'):
            for r in d.findall('r'):
                for c in r.findall('c'):
                    vals.append(c.text)
            
        return headers, vals

    def make_meter_reads_dict(self,headers,vals,equipment_id,date):
        list_of_reads = []
        for i in range(len(headers)):
            d = {}
            d['equipment_id'] = equipment_id
            d['date'] = date
            d['header'] = headers[i]
            d['value'] = vals[i]
            list_of_reads.append(d)

        return list_of_reads

    # not the best - move to dataloader
    def get_equipment_id(self, file_path):
        
        return file_path[-9:-4]

    # not the best - move to dataloader
    def get_date(self, file_path):
        
        return file_path[-35:-25]

    def load_file_to_db(self, file_path, conn):
                
        root = self.get_xml_root(file_path)

        if not root: #empty root
            return 0
        
        #columns = ['equipment_id','date','header','value']
        
        #table_name = 'meter_reads'
        
        s = self.make_sql_string(self.table_name,self.columns)

        date = self.get_date(file_path)
        
        equipment_id = self.get_equipment_id(file_path)

        headers, vals = self.parse_meter_read(root)
        
        list_of_reads = self.make_meter_reads_dict(headers,vals,equipment_id,date)
        
        self.sql_query(conn,s,list_of_reads)  

        return s
    
    '''    
    def load_files_to_db(self, file_list=None, folder=None):
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
    '''
    def single_file_test(self):
        file_path = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\eGauge\production\2020\04\2020-04-01_meter_read_for_33746.xml'
        file_path = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\eGauge\production\2020\04\2020-04-01_meter_read_for_33044.xml'
        print('starting load')
        load_single_file(file_path)
        print('load complete')

    def meter_reads_main(self):
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
