import numpy as np
import pandas as pd

def create_expected_production(system_size, in_service_date, 
                               specific_yield_per_year, annual_degradation_rate, monthly_adj, weather_adjustments):
    '''
    Docstring for create_expected_production()
    create_expected_production is the master coordinator for creating an expected production model for a single system.
    This function is responsible for coordinating helper functions to deliver 301 months of expected production.
    inputs:
    system_size: the size of the system in kW (numeric)
    in_service_date: the date of the first energy produced by the system and the start of the 25 yr life of the system (YYYY-MM-DD)
    specific_yield_per_year: the kWh/kW/yr the system is assumed to perform (numeric)
    annual_degradation_rate: the ammount of degradation per year as a decimal that the system is assumed to undergo (decimal)
    monthly_adj: the 12 month adjustments in production of the year, totaling to 1 (list of decimals)
    weather_adjustments: 301 values between -1 and 1 to adjust for weather (list of decimals)
    outputs:
    df: a pandas dataframe with 301 months as an index and the respective expected production
    '''
    # make annual production
    annual_production = system_size * specific_yield_per_year
    
    # date adjustments
    in_service_date = pd.to_datetime(in_service_date)
    first_month = pd.to_datetime(in_service_date - pd.offsets.MonthBegin(1))
    date_range = pd.date_range(start=first_month, periods=301, freq='M')
    
    # adj months
    monthly_adjustments = create_adj_13_month(in_service_date, monthly_adj)
    
    # create 25 yr production model
    production = create_301_expected_production_months(annual_production, monthly_adjustments, annual_degradation_rate)
    
    # apply weather adjustments
    weather_adjusted_expected_production = apply_weather(weather_adjustments,production)
    
    # make dates and production in df
    df = make_ep_dataframe(date_range, weather_adjusted_expected_production)
    
    return df

def create_adj_13_month(in_service_date, monthly_adj):
    # get basic date information
    first_month = in_service_date.month
    last_day_of_month = in_service_date + pd.tseries.offsets.DateOffset(months=1) - pd.tseries.offsets.DateOffset(days=in_service_date.day)
    days_in_month = last_day_of_month.day
    
    # split month one into first section and last section
    first_section_m1 = float((in_service_date.day - 1)/days_in_month)
    last_section_m1 = float((days_in_month - in_service_date.day + 1)/days_in_month)
    
    # change 12 month window
    months_13 = monthly_adj[first_month:] + monthly_adj[:first_month] 
    # add 13th month
    months_13.append(monthly_adj[first_month])
    # change the first month to a fractional month
    months_13[0] = float(months_13[0]) * last_section_m1
    # change the 13th month to a fractional month
    months_13[-1] = months_13[-1] * first_section_m1

    return months_13

def make_ep_dataframe(date_range, expected_production):
    '''
    docstring make_ep_dataframe
    ----------------------------------------------------------------------------------
    make_ep_dataframe makes a pandas dataframe with a date range of months as the index
    and the expected monthly production as a cloumn called production.
    inputs: 
    date_range: a date range of 301 months
    expected_production: the expected production values of each month
    outputs:
    df: a pandas dataframe with months as the index and expected production as columns
    '''
    d = {'date':date_range,'expected_production':expected_production}
    df = pd.DataFrame(d).set_index('date')
    return df

def create_301_expected_production_months(annual_production, months_13, annual_degradation_rate):
    
    prod = np.array([0]*301)
    
    for i in range(25):
        degradation = 1 - (i * annual_degradation_rate)
        this_year_prod = np.array([annual_production * degradation] * 13)
        temp = np.array(months_13) * this_year_prod
        if i == 0:
            prod[i*13:(i+1)*13] = temp
        else:
            prod[i*12:(i+1)*12+1] = prod[i*12:(i+1)*12+1] + temp
            
    return prod

def apply_weather(weather_adjustments,expected_production):
    # convert weather adjustments to numpy array
    weather_adj_numpy = np.ones(len(weather_adj)) - np.array(weather_adj)
    # multiply expected production
    weather_adjusted_expected_production = weather_adj_numpy * expected_production
    
    return weather_adjusted_expected_production


if __name__ == '__main__':
	in_service_date = '2020-03-14'
	annual_degradation_rate = 0.005
	specific_yield_per_year = 1250
	monthly_adj = list(pd.read_csv('monthly_production_curve.csv')['Monthly Curve'])
	system_size = 1
	weather_adj = [0,0,0,-.1,0,0,0,0,0,0,.1,0] * 25
	weather_adj.append(0)
	#np.ones(len(weather_adj)) - np.array(weather_adj)
	create_expected_production(system_size, in_service_date, 
                           specific_yield_per_year, annual_degradation_rate, monthly_adj, weather_adj)