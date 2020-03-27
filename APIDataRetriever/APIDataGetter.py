import os
import requests
import json
from functools import wraps
import time
import sys
from config import config
# sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),api_folder_name))


class APIDataConnector(object):
	"""docstring for APIDataConnector"""
	def __init__(self, 
			data_provider_company = '',
			start_date='2019-05-01',
			end_date='2019-05-02', 
			time_unit='QUARTER_OF_AN_HOUR'):

		self.get_credentials(data_provider_company)

		#self.API_KEY = self.get_api_key(data_provider_company)

		self.company_name = 'generic'

		self.equipment_company_name = 'generic'

		self.app_folder = self.get_app_dir()

		self.set_auth()

		self.start_date = start_date

		self.end_date = end_date

		self.time_unit = time_unit

	def timer(func):
	#""" Print the runtime of the decorated function """
		@wraps(func)
		
		def wrapper_timer(*args, **kwargs):
			
			start_time = time.perf_counter()    # 1
			
			value = func(*args, **kwargs)
			
			end_time = time.perf_counter()      # 2
			
			run_time = end_time - start_time    # 3
			
			print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
			
			return value
		
		return wrapper_timer

	def set_auth(self):

		self.auth = None

		try:
			if self.username and self.password:

				self.auth = (self.username,self.password)
			
		except Exception as e:
			pass
		
		pass
 
	
	def setup_directories(self, folder_path):
		
		path_existed = True

		if not os.path.exists(folder_path):
			
			os.makedirs(folder_path)
			
			print('new folder path created: ', folder_path)

			path_existed = False
		
		return path_existed

	def make_file_path(self, file_name, sub_directory=None):
				
		folder_path = os.path.join(self.app_folder, 'raw_data', self.company_name, self.equipment_company_name, sub_directory)

		self.setup_directories(folder_path)

		file_path = os.path.join(folder_path, file_name)

		return file_path


	def get_app_dir(self):
		
		return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	def get_credentials(self, data_provider_company):
		
		section = data_provider_company.lower()

		params = config(section=section)

		params.setdefault('username',None)
		
		# get initialization parameters, use none if not provided
		self.username = params.get('username',None)
		
		self.password = params.get('password',None)
		
		self.API_KEY = params.get('api_key',None)

	''' delete me '''
	def get_api_key(self, data_provider_company):

		section = data_provider_company.lower()

		params = config(section=section)

		try:
			
			API_KEY = params['api_key']

		except Exception as e:
			
			raise e
			
			API_KEY = None


		return API_KEY #None if API_KEY is None else params['api_key']

	def convert_xml_to_json(self, payload):
		# TODO: Add conversion code
		return payload

	def call_api(self, url):
		
		payload = None
		
		try:
		
			r = requests.get(url, auth = self.auth)

			#print(r)
		
			payload = r.json()
		
		except Exception as e:
		
			raise e
		
		return payload

	def post_api(self, url, data, headers=None):
		
		r = requests.post(url=url, data=data, headers=headers)
		
		if r.text:
		
			print(r.text)
		
			return True
		
		return False
		

	def verify_payload_not_empty(self, payload):
		
		empty_payload = False
		
		if not payload:
		
			print('Error: Empty Payload [write_payload method]')
		
			payload = 'Empty payload'

			empty_payload = True

		return payload, empty_payload

	def write_json_to_file(self, payload, file):

		with open(file, 'w+') as f:

			json.dump(payload, f)

		print('data succesfully written to file')

		return True

	def append_json_to_file(self,payload,file):

		pass

	def write_payload(self, payload, file_name, sub_directory):
		
		payload, empty_payload = self.verify_payload_not_empty(payload)

		file = self.make_file_path(file_name, sub_directory)
		
		clean_write = self.write_json_to_file(payload, file)
		
		return clean_write

	def load_payload_to_memory(self, file_name, sub_directory=None):
		
		file_name = self.make_file_path(file_name=file_name, sub_directory=sub_directory)
		
		with open(file_name) as json_file:
		
			data = json.load(json_file)	
		
		return data

	def convert_site_ids_to_string(self,site_list):

		s = ''

		for site in site_list:

			if s == '':

				s = str(site)

			else:

				s = s + ',' + str(site)

		return s

	def set_timing(self):
		''' Example of a change
		self.start_date = '2019-05-03'
		self.end_date = '2019-05-06'
		self.time_unit = 'QUARTER_OF_AN_HOUR'
		'''

		return self.start_date, self.end_date, self.time_unit
		#return start_date, end_date, time_unit

			
if __name__ == '__main__':

	c = APIDataConnector(data_provider_company='Solaredge')
	#print(c.username,c.password)
	print(c.API_KEY)
	print(c.app_folder)
	#print(help(c))
	print(c.set_timing())