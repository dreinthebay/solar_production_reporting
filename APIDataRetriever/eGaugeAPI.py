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

		self.start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')

		self.end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')

		self.site_name = '33740'

		self.get_site_id()

		self.REG = 'gen'

		self.data = {}


	
	def get_site_id(self):

		self.api_site = config(section='egauge')['devaddr']

		pass

	def make_api_url(self, future, past):

		url = 'http://{}/cgi-bin/egauge-show?a&T={},{}'.format(self.api_site, future, past)

		return url

	# TODO: Move this function to the APIDataGetter file
	def call_api(self, url):

		r = requests.get(url)

		if r.text:
			
			return r.text

		return None


	# TODO standardize
	def run_site_production(self):
		
		self.date_loop()
		
		file_name = '{}_production_from_{}_to_{}.json'.format(self.site_name,str(self.start_date.date()),str(self.end_date.date()))
		
		self.write_payload(self.data, file_name, 'production')
		
		return True

	# TODO
	def get_delta_energy(self, payload):

		pass

		#{'site':'1234fgasdf','data':{'units':'Wh','dates':{'2019-03-01':12341}}}

	#TODO break this method up
	def date_loop(self):
		
		cur_date = self.start_date

		self.get_site_id()

		self.data['site'] = self.site_name

		self.data['data'] = {'units':'kWh','dates':{}}

		

		print('running all dates between ', cur_date, ' and ', self.end_date,' for eGauge system ', self.site_name)


		while cur_date < self.end_date:

			print('date is now ', cur_date)

			cur_time = int(cur_date.replace(tzinfo=timezone.utc).timestamp())

			end_time = cur_time + 24*60*60 - 1

			url = self.make_api_url(end_time,cur_time)
	

			print(url)

			payload = self.call_api(url)

			#print(payload,'\n\n')

			root = ET.fromstring(payload)
			
			reg_ids = {}
			for child in root.findall('data'):
				for idx, cname in enumerate(child.findall('cname')):
					reg_ids[cname.text] = idx # we know REG is in slot idx in the data sets

			# find the two column values in the two data sets based on the idx
			now_val  = None
			then_val = None
			now_found = False
			for child in root.findall('data'): # go into data tag
			    for idx, column in enumerate(child.find('r')): # enumerate through <r> tag
			        if idx == reg_ids[self.REG]: # we found the slot of the REG
			            if not now_found: # have we already found the first 'data' tag?
			                now_val = int(column.text) # no, this is the first
			                now_found = True
			            else:
			                then_val = int(column.text) # yes, we already found the first

            # energy values are in watt-seconds (joules), convert to kWh
			diff = float((now_val - then_val)/3600000)
			print('Difference: {} kWh'.format(diff))

			key = str(cur_date.date())

			self.data['data']['dates'][key] = diff


			# average value is kWh / hours
			print('Average: {} kW'.format(diff/(24/60/60)))

			cur_date += datetime.timedelta(days=1) 

		print('finished loop')

		print('the data dictionary is')

		pprint.pprint(self.data)

		return self.data

	def special_date_loop(self):
		'''
		special date loop gets data between the start and end periods, which may not be daily.
		The api query is made, data is returned and parsed in xml for production data only (specifically gen) 
		the data is stored in a dictionary, which can later be converted into csv if necessary

		'''
		# for maulik's request for date for a month
		self.REG = 'gen'

		cur_date = self.start_date

		sites = self.load_site_keys()
		
		self.data['sites'] = {}

		i = 0

		for site in sites:
			
			if i in [7,10]:
				print('skipping {}...'.format(site))
			else:
				print('{}. {} data...'.format(i,site))

				temp = {'site':site,'data':{'units':'kWh','values':{}}}
				#self.data['site'] = self.site_name

				#self.data['data'] = {'units':'kWh','dates':{}}

				print('running all dates between ', cur_date, ' and ', self.end_date,' for eGauge system ', site)

				# run once form start date to end date of month

				cur_time = int(cur_date.replace(tzinfo=timezone.utc).timestamp())

				end_time = int(self.end_date.replace(tzinfo=timezone.utc).timestamp())
				
				self.api_site = str(site) + '.egaug.es/'

				url = self.make_api_url(end_time,cur_time)

				print(url)

				payload = self.call_api(url)

				#print(payload,'\n\n')

				root = ET.fromstring(payload)
				try:
					reg_ids = {}
					for child in root.findall('data'):
						for idx, cname in enumerate(child.findall('cname')):
							reg_ids[cname.text] = idx # we know REG is in slot idx in the data sets

					# find the two column values in the two data sets based on the idx
					now_val  = None
					then_val = None
					now_found = False
					for child in root.findall('data'): # go into data tag
					    for idx, column in enumerate(child.find('r')): # enumerate through <r> tag
					        if idx == reg_ids[self.REG]: # we found the slot of the REG
					            if not now_found: # have we already found the first 'data' tag?
					                now_val = int(column.text) # no, this is the first
					                now_found = True
					            else:
					                then_val = int(column.text) # yes, we already found the first

			        # energy values are in watt-seconds (joules), convert to kWh
					diff = float((now_val - then_val)/3600000)
					print('Difference: {} kWh'.format(diff))

					key = str(cur_date.date())

					temp['data']['values']['date'] = key
					temp['data']['values']['value'] = diff

					# average value is kWh / hours
					print('Average: {} kW'.format(diff/(24/60/60))) 

				except Exception as e:
					print('no generation found')


				self.data['sites'][i] = temp

			i += 1

		print('finished run')

		print('the data dictionary is')

		pprint.pprint(self.data)

		file_name = 'special_all_egauge_production_from_{}_to_{}.json'.format(
			str(self.start_date.date()),str(self.end_date.date()))
		
		self.write_payload(self.data, file_name, 'production')
		
		return True

	def get_csv_data_all_time(self):

		'''
		# get day of data
		future = int(self.end_date.replace(tzinfo=timezone.utc).timestamp())
		past = int(self.start_date.replace(tzinfo=timezone.utc).timestamp())
		url = 'http://{}/cgi-bin/egauge-show?c&T={},{}'.format(self.api_site, future, past)
		'''
		# get all daily production all time
		url = 'http://{}/cgi-bin/egauge-show?c'.format(self.api_site)

		print(url)
		
		r = requests.get(url)

		# check api payload
		#print(r.text[0:1000])

		# store payload
		payload = r.text
		
		# make new file
		file_name = '{0}_all_system_production_to_{1}.txt'.format(self.site_name
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

	def load_site_keys(self):
		'''
		This method will select the site names from an excel file that was provided by the company
		Returns a list of site names to be used for api calls
		'''
		file_name = 'New Columbia eGauges.xlsx'
		
		sites = pd.read_excel(file_name)
		
		#print(sites.head())
		
		sites = list(sites['Meter Name'])
		
		print('eGaguge site list: \n',sites)
		
		return sites

	def run_all_sites_date_range(self):
		
		sites = self.load_site_keys()
		
		i = 0

		for site in sites:

			print('{}. {} fetching data ...'.format(i,site))
			
			self.api_site = str(site) + '.egaug.es/'
			
			self.run_site_production()

			i += 1

		pass


	def run_all_sites(self):

		sites = self.load_site_keys()

		print('looping through sites\nS i t e \n--------------')

		i = 0

		for site in sites:
			
			print('{}. {} fetching data ...'.format(i,site))
			
			self.api_site = str(site) + '.egaug.es/'

			#if site == 'eGauge45512'
			#.egaug.es/

			if i > 8:
				try:
					self.get_csv_data_all_time()
				except Exception as e:
					raise e
					print('failed to get data from site ', site)
			i += 1

		print('end sites loop')



		


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