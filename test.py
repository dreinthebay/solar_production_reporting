from APIDataRetriever.APIDataGetter import APIDataConnector
from APIDataRetriever.SolarEdgeAPI import SolarEdgeAPI
from APIDataRetriever.SolarEdgeEnergySiteMeterAPI import SolarEdgeEnergySiteMeterAPI
from APIDataRetriever.SolarEdgeEnergyComponentAPI import SolarEdgeEnergyComponentAPI
from APIDataRetriever.eGaugeAPI import EgaugeAPI
from APIDataRetriever.EgaugeMeterRead import EgaugeMeterReads
from DBCreator.create_tables import *
from DataLoader.site_inverter_production_loader import *
from DataLoader.meter_reads_loader import *
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
	print(sesm.run_bulk_energy())

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

def eGauge_run_bulk_production_test():
	_start = '2020-03-01'
	_end = '2020-03-04'
	_end = None
	_company_name = 'NCS'
	eg = EgaugeAPI(start_date=_start,end_date=_end, company_name=_company_name)
	eg.run_bulk_production()

def eGauge_meter_read_test():
	date = '2020-04-01'
	company_name = 'NCS'
	egm = EgaugeMeterReads(date=date,company_name=company_name)
	print(egm.date)
	print(egm.run_bulk_meter_read())

def create_tables_test():
	cloud_connect = True
	print(test_connection())

def create_projects_table_test():
	cloud_connect = True
	create_projects_table(cloud_connect)

def create_all_tables_test():
	cloud_connect = True
	create_all_tables(cloud_connect)

def load_site_inverter_test():
	create_all_tables_test()
	file_path = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\SolarEdge\site_production\bulk_energy_2019-01-01.json'
	
	load_single_file(file_path)

def load_folder_to_db_test():
	#create_all_tables_test()
	folder = r'C:\Users\slin2\Documents\GitHub\solar_production_reporting\raw_data\NCS\SolarEdge\site_production'
	load_files_to_db(folder=folder)

def xml_loader_test():
	meter_reads_main()
	#meter_reads_loader.get_data(file_path)
	
def main():
	
	#LOADER
	#load_site_inverter_test()
	#load_folder_to_db_test()

	#XML loader
	xml_loader_test()


	#DB CREATOR TESTS
	#create_tables_test() # tests the connection
	#create_projects_table_test() # makes a single table
	#create_all_tables_test() # makes all tables


	# API TESTS (SOLAREDGE)
	#api_test() # tests the connection
	
	#solaredge_api_test() # tests the SE connection

	#site_list_test() # tests the site list method

	#site_meter_production_test() # tests the site meter api

	#site_component_prodution_test() # outside of scope

	#daily_site_production_load() # tests daily production load

	# EGAUGE TESTS
	#eGauge_test_dev()

	#eGauge_test_csv_dev()

	#eGauge_load_sites()

	#eGauge_run_bulk_production_test()

	#eGauge_run_all_sites()

	#special_maulik_ask()

	#eGauge_meter_read_test()


if __name__ == '__main__':
	main()