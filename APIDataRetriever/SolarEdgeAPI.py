from APIDataRetriever.APIDataGetter import APIDataConnector

# https://www.solaredge.com/sites/default/files/se_monitoring_api.pdf
#@APIDataConnector.timer
class SolarEdgeAPI(APIDataConnector):
	"""docstring for SolarEdgeAPI"""
	def __init__(self,start_date=None,end_date=None,time_unit=None,company_name=None):
		
		super().__init__(data_provider_company='SolarEdge',start_date=start_date,end_date=end_date,time_unit=time_unit)

		self.company_name = company_name

		self.equipment_company_name = 'SolarEdge'

	# required for both energy and site details
	def get_site_list(self):
	
		site_request_url = str('https://monitoringapi.solaredge.com/sites/list?api_key='+self.API_KEY)
	
		payload = self.call_api(site_request_url)
	
		return payload

	# gets site list and writes json payload to a json file
	def run_site_list(self):
		
		r = self.get_site_list()
		
		return self.write_payload(payload=r,file_name='site_list.json',sub_directory='site_list')

	def get_site_details(self, site_id):
		
		site_details_url = str('https://monitoringapi.solaredge.com/site/' + str(site_id) + '/details?api_key=' + self.API_KEY)
		
		payload = self.call_api(site_details_url)
		
		return payload

	def run_site_details(self):
		
		clean_run = True

		site_list = self.get_site_ids()

		for site_id in site_list:

			payload = self.get_site_details(site_id)

			if not self.write_payload(payload=payload, file_name='site_'+str(site_id)+'_details.json', sub_directory='site_details'):

				clean_run = False

		return clean_run

	# This method takes a site id and creates the api url to call. Returns the api payload in JSON
	def get_site_component_list(self,site_id):
		
		site_equipment_url = str('https://monitoringapi.solaredge.com/equipment/' + site_id + '/list?api_key=' + self.API_KEY)
		
		payload = self.call_api(site_equipment_url)
		
		return payload


	# Gets site list and looks through each site to get the component list. Returns true if the process ran cleanly
	# TODO: Get all sites and loop through them, collecting equipmen1t
	# Completed May 2019
	def run_all_site_equipment(self):
		
		clean_run = True
		
		site_list = self.get_site_ids()
		
		for site_id in site_list:
			
			print('getting site equipment for site ', site_id)
			
			payload = self.get_site_component_list(str(site_id))
			
			if not self.write_payload(payload=payload,file_name=str(site_id)+'_components.json',sub_directory='components'):
			
				clean_run = False

		return clean_run

	''' creates a list of all the site ids from a payload '''
	# required for both energy and site details
	def get_site_ids(self, api_payload=None):
		
		if not api_payload:

			api_payload = self.load_payload_to_memory(file_name='site_list.json', sub_directory='site_list')
		
		site_list = []
		
		for site in api_payload['sites']['site']:
		
			site_list.append(site['id'])
		
		return site_list
	
	''' Adds the component id to a payload. Used primarily in component production payloads '''
	def add_cid_to_payload(self, cid, payload):
		
		d = {'cid':cid}
		
		d['payload'] = payload
		
		return d

	''' This method gets the serial numbers of non gateway equipment for a site and returns the list '''
	def list_component_serial_numbers(self, site_id):
		
		file_name = str(site_id) + '_components.json'
		
		data = self.load_payload_to_memory(file_name=file_name, sub_directory='components')		
		
		serial_list = []
		
		for unit in data['reporters']['list']:
		
			if 'Gateway' not in unit['name']:
		
				serial_list.append(unit['serialNumber'])
		
		return serial_list

	
if __name__ == '__main__':
	a = APIDataConnector('username','rigetr','asdaxcjhqadsfhqweoipufuda')
	company_name = ''
	API_KEYS = {'ncs':'','':''}
	s = SolarEdgeAPI(API_KEY=API_KEYS[company_name], company_name=company_name)
	print(s.username, s.password)
	print(s.API_KEY)
	print(s.app_folder)
	print(s.company_name)
	print(s.run_site_list())
	#print(help(s))
	#print(s.run_all_site_equipment())
	#print(s.run_all_component_energy())
	#print(s.list_component_serial_numbers('225542'))
	#print(s.run_inverter_technical_data())
	#print(s.run_bulk_energy())
'''
powerdash
map
reporting
powerscout
solaredge sites flips the inverters (single phase inverters, a bus may have a bunch of inverters)
'''