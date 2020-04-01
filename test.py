from APIDataRetriever.APIDataGetter import APIDataConnector
from APIDataRetriever.SolarEdgeAPI import SolarEdgeAPI
from APIDataRetriever.SolarEdgeEnergySiteMeterAPI import SolarEdgeEnergySiteMeterAPI
from APIDataRetriever.SolarEdgeEnergyComponentAPI import SolarEdgeEnergyComponentAPI
from APIDataRetriever.eGaugeAPI import EgaugeAPI
import pprint

from config import config

def api_test(data_provider_company='SolarEdge'):
	
	print('testing api key config in APIDataConnector...')
	
	data_provider_company = 'SolarEdge'

	c = APIDataConnector(data_provider_company=data_provider_company)

	key_test = c.API_KEY
	
	key_real = config(section=data_provider_company.lower())['api_key']
	
	if key_test == key_real:
	
		print('api_key test passed')
	
		return 1
	
	#print(key_test, key_real)
	
	print('api_key test failed')
	
	return 0

def solaredge_api_test():

	print('Testing SolarEdgeAPI')

	se = SolarEdgeAPI()


	if se:
		print('SolarEdgeAPI object created.')
	else: 
		print('could not instantiate SolarEdgeAPI')
		return 0

	test_bool = se.API_KEY==config(section='solaredge')['api_key']
	if test_bool:
		print('API key match is: ', test_bool)
	else:
		print('wrong api key')
		return 0
		
	print('testing site list call')
	try:
		site_list = se.get_site_list()
	except:
		site_list = None
	
	if site_list:
		print('site list api call returned data')
		print('a sample of the site list: \n')

		site_list = pprint.pformat(site_list)
		pprint.pprint(site_list[0:2000])
	else:
		print('Failed SolarEdge API call to site list.')
		return 0

	return 1

def site_list_test():
	se = SolarEdgeAPI(company_name='test_company_name')

	se.run_site_list()

def site_meter_production_test():
	_start = '2020-03-01'
	_end = '2020-03-02'
	_timeunit = 'QUARTER_OF_AN_HOUR'
	sesm = SolarEdgeEnergySiteMeterAPI(company_name='test_company_name',start_date=_start,end_date=_end,time_unit=_timeunit)

	#sesm.get_bulk_energy()
	sesm.run_bulk_energy()

def site_component_prodution_test():
	
	scp = SolarEdgeEnergyComponentAPI(company_name='test_company_name')
	print(scp.company_name)
	scp.run_all_component_energy()

def daily_site_production_load():
	_start = '2020-03-01'
	_end = '2020-03-02'
	_timeunit = 'DAY'
	sesm = SolarEdgeEnergySiteMeterAPI(company_name='test_company_name',start_date=_start,end_date=_end,time_unit=_timeunit)
	sesm.run_bulk_energy()

def eGauge_test_dev():
	_start = '2020-03-01'
	_end = '2020-03-04'
	eg = EgaugeAPI(start_date=_start,end_date=_end)

	print(eg.start_date)

	#eg.date_loop()

	eg.run_site_production()

def eGauge_load_sites():
	_start = '2020-03-01'
	_end = '2020-03-04'
	eg = EgaugeAPI(start_date=_start,end_date=_end)
	eg.load_site_keys()

def eGauge_test_csv_dev():
	_start = '2020-03-01'
	_end = '2020-03-04'
	eg = EgaugeAPI(start_date=_start,end_date=_end)

	print(eg.start_date)

	#eg.date_loop()

	#eg.run_site_production()

	eg.get_csv_data_all_time()

def eGauge_run_all_sites():
	_start = '2020-03-01'
	_end = '2020-03-04'
	eg = EgaugeAPI(start_date=_start,end_date=_end)

	eg.run_all_sites()


def special_maulik_ask():
	_start = '2020-02-01'
	_end = '2020-03-01'
	eg = EgaugeAPI(start_date=_start,end_date=_end)
	eg.special_date_loop()


def main():

	#api_test()
	
	#solaredge_api_test()

	#site_list_test()

	#site_meter_production_test()

	#site_component_prodution_test()

	#daily_site_production_load()

	eGauge_test_dev()

	#eGauge_test_csv_dev()

	#eGauge_load_sites()

	#eGauge_run_all_sites()

	#special_maulik_ask()

if __name__ == '__main__':
	main()