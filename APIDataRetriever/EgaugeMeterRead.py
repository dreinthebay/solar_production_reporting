import datetime
from datetime import timezone
from APIDataRetriever.eGaugeAPI import EgaugeAPI

class EgaugeMeterReads(EgaugeAPI):
	"""docstring for EgaugeMeterReads"""
	def __init__(self, date, company_name='NCS'):
		super(EgaugeMeterReads, self).__init__(start_date=date,end_date=None,company_name=company_name)
		self.date = datetime.datetime.strptime(date, '%Y-%m-%d')

		
	def run_bulk_meter_read(self):
		clean_run = True # true if no errors during run, false if any error

		date = self.date # the start date, in the past
		
		sites = self.get_site_list() # gets all egauge sites
		
		file_site_dict = {} # initialize dictionary of sites and payloads
		
		i = 0 # iterater for debugging
		
		# loop through all sites and get production
		for site in sites:
		
			print('{}. {} fetching data ...'.format(i,site))
		
			success, file_path = self.run_site_meter_read(site, date)

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


	def run_site_meter_read(self, site_id, date):

		unix_date = int(date.replace(tzinfo=timezone.utc).timestamp()) 
		
		payload = self.get_meter_read(site_id, unix_date)
		
		file_name = '{date}_meter_read_for_{sid}.xml'.format(date=str(date.date()), sid=site_id)
		
		return self.write_payload(payload,file_name,'production')

	def get_meter_read(self,site_id,unix_date):
		
		meter_read_url = 'http://egauge{site_id}.egaug.es//cgi-bin/egauge-show?a&T={unix_date}'.format(
				site_id=site_id,unix_date=unix_date)
		
		payload = self.call_api(meter_read_url)
		
		return payload
