from APIDataRetriever.SolarEdgeEnergySiteMeterAPI import SolarEdgeEnergySiteMeterAPI
from APIDataRetriever.eGaugeAPI import EgaugeAPI
import datetime


end_date = (dt.datetime.today() - dt.timedelta(days=2)).strftime('%Y-%m-%d')

start_date = (dt.datetime.today() - dt.timedelta(days=3)).strftime('%Y-%m-%d')

print('running eGaugeAPI for all sites daily production between ', start_date, ' and ', end_date)

myEgaugeAPI = EGaugeAPI(start_date=start_date, end_date=end_date)
myEgaugeAPI.run_all_sites()

args = {
'start_date':start_date,
'end_date':end_date,
'time_unit':'DAY',
'company_name':'NCS'
}

print('running SolarEdgeAPI for all sites daily production between ', start_date, ' and ', end_date)

mySolarEdge = SolarEdgeEnergySiteMeterAPI(**args)

seesma.run_site_list()
seesma.run_bulk_energy()

print('complete')