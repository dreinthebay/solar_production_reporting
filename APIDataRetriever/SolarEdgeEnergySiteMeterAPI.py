from APIDataRetriever.SolarEdgeAPI import SolarEdgeAPI

class SolarEdgeEnergySiteMeterAPI(SolarEdgeAPI):
	"""docstring for SolarEdgeEnergySiteMeterAPI"""
	def __init__(self, start_date='2019-05-01', end_date='2019-05-02', time_unit='QUARTER_OF_AN_HOUR', company_name='NCS'):

		super(SolarEdgeEnergySiteMeterAPI, self).__init__(start_date=start_date, end_date=end_date, time_unit=time_unit, company_name=company_name)
	
	#def get_bulk_energy(self,start_date,end_date,time_unit):
	def get_bulk_energy(self):
		
		site_list = self.get_site_ids()
	
		# make string
		string_of_site_ids = self.convert_site_ids_to_string(site_list)
	
		bulk_energy_url = str('https://monitoringapi.solaredge.com/sites/' + string_of_site_ids + '/energy?timeUnit=' + self.time_unit
		 + '&startDate=' + self.start_date + '&endDate=' + self.end_date + '&api_key=' + self.API_KEY)

		print('\n\n',bulk_energy_url,'\n\n')

		payload = self.call_api(bulk_energy_url)
		
		return payload

	#@APIDataConnector.timer
	# Site Energy - Detailed
	def run_bulk_energy(self):

		time_args = self.set_timing()

		print('time_args: ', time_args)

		#r = self.get_bulk_energy(*time_args)
		r = self.get_bulk_energy()

		file_name = 'bulk_energy_' + self.start_date + '.json'

		success, file_path = self.write_payload(payload=r, file_name=file_name, sub_directory='site_production')
		
		return success, file_path
	
if __name__ == '__main__':

	company_name = ''
	
	API_KEYS = {'':''}
	
	args = {'API_KEY': API_KEYS[company_name],'start_date':'2020-02-01', 'end_date':'2020-02-29',
	
	'time_unit':'QUARTER_OF_AN_HOUR', 'company_name':company_name}
	
	s = SolarEdgeEnergySiteMeterAPI(**args)

	print(s.start_date)

	print(s.company_name)
	
	print(s.run_bulk_energy())

	#print(help(s))