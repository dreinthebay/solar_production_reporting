from APIDataRetriever.SolarEdgeAPI import SolarEdgeAPI

class SolarEdgeEnergyComponentAPI(SolarEdgeAPI):
	"""docstring for SolarEdgeEnergyComponentAPI"""
	def __init__(self, start_date='2019-05-01', end_date='2019-05-02', time_unit='QUARTER_OF_AN_HOUR', company_name='NCS'):
		
		super(SolarEdgeEnergyComponentAPI, self).__init__(start_date=start_date, end_date=end_date, time_unit=time_unit, company_name=company_name)
	
	''' deprecated '''
	def get_component_energy(self, site_id):

		energy_url = 'https://monitoringapi.solaredge.com/site/'+str(site_id)+'/energyDetails?meters=PRODUCTION&timeUnit='+self.time_unit + \
			'&startTime='+self.start_date+' 00:00:00&endTime='+self.end_date+' 00:00:00&api_key='+self.API_KEY

		payload = self.call_api(energy_url)

		return payload

	''' deprecated '''
	#@APIDataConnector.timer
	def run_all_component_energy(self):

		site_list = self.get_site_ids()

		for site_id in site_list:

			print('Getting component data for site ', site_id)

			payload = self.get_component_energy(site_id)

			self.write_payload(payload=payload, file_name=str(site_id) + '_component_production_'+self.start_date + ".json",sub_directory='component_production')

		return True

	def get_inverter_technical_data(self, site_id, serial_id):

		inverter_url = 'https://monitoringapi.solaredge.com/equipment/'+str(site_id)+' /'+serial_id+'/data?startTime='+ \
			self.start_date+' 00:00:00&endTime='+self.end_date+' 00:00:00&api_key='+self.API_KEY

		#print(inverter_url)

		payload = self.call_api(inverter_url)

		return payload

	
	#@APIDataConnector.timer
	# The component production
	#''' For each site, for each piece of equipment, get the inverter technical data '''
	# TODO: Add time_args
	def run_inverter_technical_data(self):
		
		site_list = self.get_site_ids()
		
		print(site_list)
		
		for site_id in site_list:
		
			if str(site_id) != '420924': # it takes only 20 seconds to load this site
			#if str(site_id): # it takes about 340 seconds to load all the data
		
				component_serial_number_list = self.list_component_serial_numbers(site_id=site_id)
		
				for serial_id in component_serial_number_list:
		
					print('writing serial_id ', serial_id, ' from site ', site_id, ' to file...')
		
					initial_dictionary = self.get_inverter_technical_data(str(site_id), serial_id)
		
					payload = self.add_cid_to_payload(serial_id, initial_dictionary)

					#print(payload)
		
					self.write_payload(payload=payload, file_name='sid_'+str(site_id) +'_cid_' +serial_id+ '_production_'+self.start_date+'.json', sub_directory='component_production')

		return True		

