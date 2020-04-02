from ProductionLoader import ProductionLoader

class SolarEdgeSiteProductionLoader(ProductionLoader):
	"""docstring for SolarEdgeSiteProductionLoader"""
	def __init__(self,cloud_connect=False, company_name='MassAm'):
		super(SolarEdgeSiteProductionLoader, self).__init__(company_name=company_name)
		
		self.equipment_company_name = 'SolarEdge'
		
		self.energy_unit = 'Wh'
		
		self.cloud_connect = cloud_connect

	
	"""
	get production data
	make sql query
	connect to postgres
	execute query
	"""

	def make_sql_string(self, data):
		
		sql = """INSERT INTO public.production (site_id, measured_by, unit, value, date) VALUES """

		energy_unit = data['sitesEnergy']['unit']

		site_id = data['sitesEnergy']['siteEnergyList'][0]['siteId']
		
		for site in data['sitesEnergy']['siteEnergyList']:
			
			site_id = site['siteId']
			
			measured_by = site['energyValues']['measuredBy']
			
			for val in site['energyValues']['values']:
			
				value = val['value']
				
				if not value:
					value = 'Null'
			
				date = val['date']

				sql += '(\'{0}\',\'{1}\',\'{2}\',{3},\'{4}\'), '.format(site_id, measured_by, energy_unit, value, date)
		
		sql = sql[:-2]

		return sql

if __name__ == '__main__':
	pd = SolarEdgeSiteProductionLoader(cloud_connect=True,company_name='Barrier')
	print(pd.company_name)
	print('cloud_connect = ',pd.cloud_connect)
	
	# test full folder load
	print(pd.run_total_production_table_loader(sub_directory='site_production'))
	
	# test single file load
	'''
	file = 'bulk_energy_2019-05-01.txt'
	sub_directory = 'site_production'
	pd.run_single_batch(file,sub_directory)
	'''
	'''
	files = ['050_bulk_energy_2016-07-01.txt','050_bulk_energy_2016-08-01.txt',
	'050_bulk_energy_2016-09-01.txt','050_bulk_energy_2016-10-01.txt','050_bulk_energy_2016-11-01.txt',
	'050_bulk_energy_2016-12-01.txt','050_bulk_energy_2017-01-01.txt','050_bulk_energy_2017-02-01.txt',
	'050_bulk_energy_2017-03-01.txt','050_bulk_energy_2017-04-01.txt','050_bulk_energy_2017-05-01.txt',
	'050_bulk_energy_2017-06-01.txt']
	sub_directory = 'site_production'
	for file in files:
		pd.run_single_batch(file, sub_directory)
	'''
	#data = pd.get_production_data(file,sub_directory)
	#s = pd.make_sql_string(data)
	#print(s[0:200])