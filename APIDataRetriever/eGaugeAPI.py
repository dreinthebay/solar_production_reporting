from APIDataRetriever.APIDataGetter import APIDataConnector
from config import config
import requests
import time
import datetime
from datetime import timezone
import xml.etree.ElementTree as ET # to parse XML
import pprint # used for testing, can remove
import csv # unused for testing
import pandas as pd # for excel loading, parsing
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError


#class EgaugeAPI(object):
class EgaugeAPI(APIDataConnector):
	"""docstring for EgaugeAPI
eGauge documentation can be found here
https://www.egauge.net/media/support/docs/egauge-xml-api.pdf

Important information from params in API documentation

d n/a Specifies that n and s parameters are specified in units of days.
n Integer (U32) Specifies the maximum number of rows to be returned.
f Integer (U32) Specifies the timestamp of the first row to be returned.
t Integer (U32) Specifies the timestamp of the last row to be returned.

	"""
	def __init__(self, start_date, end_date, company_name='NCS'):
		
		super(EgaugeAPI, self).__init__(data_provider_company='eGauge',start_date=start_date,end_date=end_date)
		
		self.company_name = company_name

		self.equipment_company_name = 'eGauge'

		self.start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d') if start_date else None

		self.end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d') if end_date else None

		self.error_list = []


	# TODO: Move this function to the APIDataGetter file
	# TODO: remove text, handle api results better
	# TODO: handle errors from requests
	# https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
	# https://stackoverflow.com/questions/9054820/python-requests-exception-handling
	def call_api(self, url):

		try:
		
			r = requests.get(url)#, timeout=15)
		
		except requests.exceptions.ConnectionError as e:
		#except requests.exceptions.ConnectTimeout as e:
			
			print('\n\n\n\n\n\nConnection TIME OUT \n',url,'\n\n\n\n\n\n\n')

			self.error_list.append(url)
		
			return ''

		if r.text:
			
			return r.text

		return None

	def write_payload(self, payload, file_name, sub_directory):
		
		payload, empty_payload = self.verify_payload_not_empty(payload)

		file = self.make_file_path(file_name, sub_directory)

		if str(file_name)[-3:].lower() == 'csv':
			#print('in csv write...')
			clean_write = self.write_csv_to_file(payload, file)
		
		else:
		
			clean_write = self.write_xml_to_file(payload, file)
		
		return clean_write, file

	def write_xml_to_file(self, payload, file):
	
		try:
	
			with open(file, 'w') as f:
	
				f.write(payload)
	
			return True
	
		except Exception as e:
	
			raise e
	
		return False
	
	def load_site_keys(self):
		'''
		This method will select the site names from an excel file that was provided by the company
		Returns a list of site names to be used for api calls
		'''
		file_name = 'New Columbia eGauges.xlsx'
		
		sites = pd.read_excel(file_name)
		
		#print(sites.head())
		
		# gets list of items ex. eGauge44712
		sites = list(sites['Meter Name'])

		# select only site id ex. 44712
		sites = list(map(lambda x: x[-5:],sites))
		
		print('eGaguge site list: \n',sites)
	
		return sites

	def get_site_list(self):

		sites = self.load_site_keys()

		ignore_list = self.load_ignored_sites()

		non_ignored_sites = []

		non_ignored_sites = [x for x in sites if x[0] not in ignore_list] # fancy

		'''
		non_ignored_sites = []

		for site in sites:

			if site not in ignore_list:

				non_ignored_sites.append(site)
		'''
		return non_ignored_sites

	def load_ignored_sites(self):

		file_name = 'system_ignore_list.csv'

		df = pd.read_csv(file_name)

		ignore_list = list(df['Ignore list'])

		return ignore_list

	def get_csv_data_all_time(self, site_id):

		'''
		This function gets data from all time, regardless of date range passed to the object
		This function works for only one site
		# 
		get day of data
		future = int(self.end_date.replace(tzinfo=timezone.utc).timestamp())
		past = int(self.start_date.replace(tzinfo=timezone.utc).timestamp())
		url = 'http://{}/cgi-bin/egauge-show?c&T={},{}'.format(self.api_site, future, past)
		'''
		# get all daily production all time
		url = 'http://egauge{}.egaug.es//cgi-bin/egauge-show?c'.format(site_id)

		print(url)
		
		r = requests.get(url)

		# check api payload
		#print(r.text[0:1000])

		# store payload
		payload = r.text
		
		# make new file
		file_name = '{0}_all_system_production_to_{1}.csv'.format(site_id
			,self.end_date.date())
		sub_directory = 'production'
		file = self.make_file_path(file_name, sub_directory)


		# this method contains extra lines
		# Write to .CSV
		#with open(file, 'w+') as f:

		#	f.write(r.text)
			
		#print('data succesfully written to file')

		# remove extra lines from payload
		payload = "\n".join(r.text.splitlines())
		'''
		# write to file
		with open(file, 'w+') as f:

			f.write(payload)
			
		print('data succesfully written to file')
		'''
		# this needs to be re-written because it writes json only
		print('testing write payload')
		print('file_name = ',file_name)
		#print()
		return self.write_payload(payload, file_name, 'production')



		


# need site id 
# need api key

'''
api call format
http://[basesiteid]//cgi-bin/egauge?[params]
[basesiteid] = the 5 number identifier. this is similar to an api key
[params] = the parameters for the api call, separated with a &

example api call
http://egauge37006.egaug.es//cgi-bin/egauge?tot
'''

'''
idea
for each system
have a start date and end date
for each day between dates
call api for data between midnight and 11:59:59
get the difference of that data
store the result in a dictionary
store the dictionary as json?
increment date

'''