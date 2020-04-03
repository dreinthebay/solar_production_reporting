from DataLoader import DataLoader
import os

class ProductionLoader(DataLoader):
	"""docstring for ProductionLoader
	This class loads production for solaredge and powerdash components 
	"""
	def __init__(self, cloud_connect=False, company_name='NCS'):
		super(ProductionLoader, self).__init__(cloud_connect=cloud_connect, company_name=company_name)

		self.equipment_company_name = 'generic'

		#self.company_name = company_name

		#self.cloud_connect = cloud_connect

		self.conn = None
	
	""" Returns the production data for a file name as a dictionary. Upgraded get_json method """
	def get_production_data(self, file_name, sub_directory='site_production'):

		data = self.get_json_data(file_name, sub_directory)

		return data
	
	''' This is an interface method that needs to be written in the child class '''
	def make_sql_string(self, data):
		
		sql = ''
		
		return sql

	'''This method executes the component production load for one file through the following process
	get production data
	create a sql insert into statement 
	connect to postgres
	execute the insert into statement
	returns if the process was successful T/F '''
	def run_single_batch(self, file_name, sub_directory):
		
		success = False

		data = self.get_production_data(file_name, sub_directory)

		sql = self.make_sql_string(data)

		
		if not self.conn:
		
			self.connect_to_postgres()

		success = self.execute_insert_query(sql)

		return success

	''' Runs single batch production load for every file in a folder '''
	def run_total_production_table_loader(self,sub_directory='site_production'):
		
		site_folder = self.get_file_path(file_name='',sub_directory=sub_directory)
		
		self.connect_to_postgres()

		print('running total production for components in folder ', site_folder)
		
		for file_name in os.listdir(site_folder):

			#print('Loading data from file ', file_name)

			self.run_single_batch(file_name, sub_directory)

		self.disconnect()

		return True

	'''deprecated methods '''
	
	'''
	def energy_bulk_runner(self):
		perfect_run = True
		#get all data
		data = self.energy_dict_by_site_list(self.get_data())

		if self.connect_to_postgres():

			for d in data:
				
				site_id, measured_by, values = self.energy_parameters(d)
				
				success = self.energy_create_then_execute_bulk_query(site_id, measured_by, values)

				if not success: perfect_run = False
		
			self.disconnect()

		return perfect_run

	def energy_parameters(self,data):
		# maps the energy data
		site_id = ''
		measured_by = ''
		value = ''
		return site_id, measured_by, value

	def energy_create_then_execute_bulk_query(self, component_id, measured_by, values):
		
		print('creating queries for component id: ', component_id)

		queries = self.energy_make_bulk_queries_string(component_id, measured_by, values)
				
		success = self.execute_bulk_queries_fast(queries)
		
		print('Query execution was success: ', success)

		return success

	def energy_make_bulk_queries(self,site_id,measured_by,values):
		
		queries = []
		
		for value in values:
		
			query = (site_id, measured_by, self.energy_unit, str('\''+value['date']+'\''), value['value'])
		
			queries.append(query)
		
		return queries

	def energy_make_bulk_queries_string(self, site_id, measured_by,values):
		
		queries = ''

		for value in values:

			if not value['value']:
				v = 'Null'
			else:
				v = value['value']

			if queries == '':
				# first query
				queries = '({0},\'{1}\',\'{2}\',{3},{4})'.format(site_id, measured_by, self.energy_unit, str('\''+value['date']+'\''), v)
				print(queries)
			
			else:
			
				queries = queries + ', ({0},\'{1}\',\'{2}\',{3},{4})'.format(site_id, measured_by, self.energy_unit, str('\''+value['date']+'\''), v)
		
		print(queries[0:99])
		return queries
	'''

if __name__ == '__main__':
	pl = ProductionLoader()
	print(pl.company_name)
