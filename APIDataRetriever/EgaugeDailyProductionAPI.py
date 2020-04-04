import datetime
from datetime import timezone
from APIDataRetriever.eGaugeAPI import EgaugeAPI

class EgaugeDailyProductionAPI(EgaugeAPI):
	"""docstring for EgaugeDailyProductionAPI"""
	def __init__(self, start_date, end_date, company_name='NCS'):
		super(EgaugeDailyProductionAPI, self).__init__(company_name=company_name,start_date=start_date,end_date=end_date)
		
	def run_site_production(self,site_id,start_date,end_date):
		'''
		retrieves and writes raw data to production file
		returns success of file write and the full path of the new file
		'''
		unix_start_date = int(start_date.replace(tzinfo=timezone.utc).timestamp()) 

		unix_end_date = int(end_date.replace(tzinfo=timezone.utc).timestamp())

		payload = self.get_site_production(site_id, unix_start_date, unix_end_date)

		file_name = '{start}_to_{end}_production_for_{sid}.xml'.format(
			
			start=str(start_date.date()), end=str(end_date.date()), sid=site_id)

		return self.write_payload(payload, file_name, 'production')

	def run_bulk_production(self):
		'''
		retrieves and writes data for each site
		returns whether the run had no errors (boolean) and a dictionary of each site name and full filepath of payload
		'''
		clean_run = True # true if no errors during run, false if any error

		start_date = self.start_date # the start date, in the past
		
		end_date = self.end_date # the end date, more recent
		
		sites = self.get_site_list() # gets all egauge sites
		
		file_site_dict = {} # initialize dictionary of sites and payloads
		
		i = 0 # iterater for debugging
		
		# loop through all sites and get production
		for site in sites:
		
			print('{}. {} fetching data ...'.format(i,site))
		
			success, file_path = self.run_site_production(site,start_date,end_date)

			print(success, file_path)
		
			if success:
		
				file_site_dict[site] = file_path
		
			else:
				# TODO: make better error handling
				# throw errors
				print('FAILURE TO LOAD SITE ',site)
		
				self.error_list.append(site) # append to error list?
		
				file_site_dict[site] = None # add empty entry
		
				clean_run = False # add flag
		
			i += 1

		print('\n\n\n\n\n\n\n\n\n\nERROR LIST:\nThese sites had errors in data fetching...\n',self.error_list)
		
		return clean_run, file_site_dict

	def get_site_production(self,site_id,start_date,end_date)
		
		site_production_xml_url = 'http://egauge{site_id}.egaug.es//cgi-bin/egauge-show?a&T={end_date},{start_date}'.format(
				
				site_id=site_id, end_date=end_date, start_date=start_date)

		print(site_production_xml_url)

		payload = self.call_api(site_production_xml_url)

		return payload
