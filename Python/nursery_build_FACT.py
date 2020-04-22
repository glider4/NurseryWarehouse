#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build main FACT table (NURSERY_ANALYSIS) based on dimension tables already
built in the nursery_transform script.
"""

import pandas as pd

# Set paths to transformed/cleaned data files
facilities_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/FACILITY.csv'
climate_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/CLIMATE.csv'
location_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/LOCATION.csv'
chemical_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/CHEMICAL.csv'
#date_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/DATE.csv'

# Import clean data files
facilities = pd.read_csv(facilities_path, delimiter=',')
climate = pd.read_csv(climate_path, delimiter=',')
location = pd.read_csv(location_path, delimiter=',')
chemical = pd.read_csv(chemical_path, delimiter=',')

climate.columns = ['ID', 'State', 'Month', 'Year', 'AvgTempC', 'AbnormalHiFlag', 'AbnormalLoFlag']


# FacilityID = LocationID = Facility_Ref

columns = ['Facility_ID', 'Location_ID', 'Climate_ID', 'Chemical_ID', 'Date_ID',
           'AvgChemDischargeLimit', 'AvgSeasonLength', 'AvgMonthlyTemp',
           'PrcntChemsMonitored', 'NumChemsDischarged', 'NumAbnormalHi',
           'NumAbnormalLo']

climate_reporting_year = climate[(climate['Year'] == 2010)]

NURSERY_ANALYSIS = pd.DataFrame(columns=columns)
    
for _ID in facilities.ID:
    
    state_abbr = location.iloc[_ID]['state_abbr']
    
    # Climate info for whatever state facility is in
    climate_avg_year = climate_reporting_year[(climate_reporting_year['State'] == state_abbr)]
    avg_C = climate_avg_year['AvgTempC'].mean()
    
    # Season is months with avg temp at 10 degrees C (50 F) or higher    
    temp_limit = climate_avg_year.apply(lambda x: True if x['AvgTempC'] >= 10 else False , axis=1)
    season_length = len(temp_limit[temp_limit == True].index)
    
    # Number of chems discharged
    if facilities.iloc[_ID]['LIKELY_TO_DISCHARGE_N_OR_P']:
        NP = 2
    else:
        NP = 0
        
    # I only want chemical info where there are limits (dropna thresh is 4 columns full) 
    chems_IDs = chemical.dropna(thresh=4)
    chems_specific = len(chems_IDs[(chems_IDs['ID'] == _ID)])
    
    # This logic fixes a bug where NP was counted twice
    if NP == 0:
        total_chems = chems_specific
    elif NP == 2:
        total_chems = NP + chems_specific
        
    # Fixes divide by zero error when finding percent of monitored chems 
    if total_chems == 0:
        percent_chems = 0
    else:
        percent_chems = chems_specific / total_chems
        
    # Average chem limit
    subset_for_numeric = chems_IDs[chems_IDs.MaxLimit.apply(lambda x: x.isnumeric())]
    subset_for_avg = subset_for_numeric[(chems_IDs['ID'] == _ID)]

    avg_chem_limit = subset_for_avg['MaxLimit'].mean()
    
    if avg_chem_limit == 'inf':
        avg_chem_limit = 'None'
    

    
    info = {'Facility_ID': _ID,
           'Location_ID': location.iloc[_ID]['ID'] , 
           'Climate_ID':  climate_avg_year[(climate_avg_year['State'] == state_abbr)].iloc[0]['ID'],
           'Chemical_ID': chemical.iloc[_ID][0], 
           'Date_ID': 0,
           'AvgChemDischargeLimit': avg_chem_limit, 
           'AvgSeasonLength': season_length, 
           'AvgMonthlyTemp': avg_C,
           'PrcntChemsMonitored': percent_chems, 
           'NumChemsDischarged': total_chems, 
           'NumAbnormalHi': 0,
           'NumAbnormalLo': 0}
    

    NURSERY_ANALYSIS = NURSERY_ANALYSIS.append(info, ignore_index=True)
    
    
NURSERY_ANALYSIS.to_csv(path_or_buf='C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/NURSERY_ANALYSIS.csv', index=False, encoding='utf-8')

