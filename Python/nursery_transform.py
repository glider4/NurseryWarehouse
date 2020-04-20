#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean up & transform nursery data; prepare to load into postgres database.
Create fact table structure and populate with data from cleaned datasets.
"""

import pandas as pd


# Set paths to data files
facilities_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/raw_data/Facilities_Likely_NP.csv'
estuaries_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/raw_data/impairedestuaries.xlsx'
rivers_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/raw_data/impairedrivers.xlsx'
lakes_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/raw_data/impairedlakes.xlsx'
waters_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/raw_data/Waters_Listed_NP_Impairments.csv'
NOAA_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/raw_data/NOAA_GHCND_subset.csv'


# Import data files as DataFrames
facilities = pd.read_csv(facilities_path, delimiter=',', encoding='iso-8859-1')
estuaries = pd.read_excel(estuaries_path, skiprows=2)
rivers = pd.read_excel(rivers_path, skiprows=2)
lakes = pd.read_excel(lakes_path, skiprows=2)
waters = pd.read_csv(waters_path, delimiter=',', encoding='iso-8859-1')
NOAA = pd.read_csv(NOAA_path, delimiter=',', encoding='iso-8859-1')

# Rename columns for estuaries, rivers, lakes df's
del estuaries['Unnamed: 7']
del estuaries['Unnamed: 8']

estuaries.columns = ['State','AssessedEstuariesSqMi','PrcntAssessedEstuaries',
                     'EstuariesWithNutrientImpairSqMi','PrctEstuariesImpaired',
                     'PrcntEstuariesImparedwithRestorationPlan', 'EstuariesReportYear']

rivers.columns = ['State','AssessedRiversMi','PrcntAssessedRivers',
                     'RiversWithNutrientImpairMiles','PrctRiversImpaired',
                     'PrcntRiversImparedwithRestorationPlan', 'RiversReportYear']

lakes.columns = ['State','AssessedLakesAcres','PrcntAssessedLakes',
                     'LakesWithNutrientImpairAcres','PrctLakesImpaired',
                     'PrcntLakesImparedwithRestorationPlan', 'LakesReportYear']

NOAA.columns = ['State', 'Month', 'Year', 'AvgTempC']


# Use index of facilities to help join fact tables later on
facilities['ID'] = facilities.index

# Subset data into multiple tables
facility = facilities[['ID','UIN','EXTERNAL_PERMIT_NMBR','PERMIT_TYPE_CODE','FACILITY_NAME','FACILITY_TYPE_INDICATOR',
                       'FACILITY_DETAIL_LINK','LIKELY_TO_DISCHARGE_N_OR_P',
                       'HAS_N_LIMITS','HAS_P_LIMITS','HAS_N_MONITORING','HAS_P_MONITORING',
                       'SICCODE','NAICS_CODE','MAJOR_MINOR_STATUS_FLAG',
                       'TOTAL_DESIGN_FLOW_NMBR', 'ACTUAL_AVERAGE_FLOW_NMBR']]

# Subset location data
facilities.rename(columns={'GOECODE_LATITUDE':'GEOCODE_LATITUDE'}, inplace=True)
location_fac_info = facilities[['ID','CITY','STATE_CODE','ZIP',
                       'COUNTY_NAME','EPA_REGION_CODE',
                       'GEOCODE_LATITUDE', 'GEOCODE_LONGITUDE']]

# Subset chemical data into wide df with all chemicals and limits
chemical_wide = facilities[['ID','TOTAL_N_MIN_LIMIT','TOTAL_N_MAX_LIMIT','TOTAL_N_LIMIT_UNITS',
                       'TKN_MIN_LIMIT','TKN_MAX_LIMIT','TKN_LIMIT_UNITS','ORGN_MIN_LIMIT',
                       'ORGN_MAX_LIMIT','ORGN_LIMIT_UNITS','AMMONIA_MIN_LIMIT',
                       'AMMONIA_MAX_LIMIT','AMMONIA_LIMIT_UNITS','INORGN_MIN_LIMIT',
                       'INORGN_MAX_LIMIT','INORGN_LIMIT_UNITS','NITRATE_MIN_LIMIT',
                       'NITRATE_MAX_LIMIT','NITRATE_LIMIT_UNITS','TOTAL_P_MIN_LIMIT',
                       'TOTAL_P_MAX_LIMIT','TOTAL_P_LIMIT_UNITS','PO4_MIN_LIMIT','PO4_MAX_LIMIT',
                       'PO4_LIMIT_UNITS']]

# Merge lakes, rivers, estuaries data together
merge_lakes_rivers = pd.merge(lakes, rivers, how='left', on=['State', 'State'])
impaired = pd.merge(merge_lakes_rivers, estuaries, how='left', on=['State', 'State'])

# List of states and their abbreviations
state_list = {'Alaska': 'AK', 'Alabama': 'AL', 'Arkansas': 'AR', 
              'American Samoa': 'AS', 'Arizona': 'AZ', 'California': 'CA', 
              'Colorado': 'CO', 'Connecticut': 'CT', 'District of Columbia': 'DC', 
              'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU', 
              'Hawaii': 'HI', 'Iowa': 'IA', 'Idaho': 'ID', 'Illinois': 'IL', 
              'Indiana': 'IN', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 
              'Massachusetts': 'MA', 'Maryland': 'MD', 'Maine': 'ME', 'Michigan': 'MI', 
              'Minnesota': 'MN', 'Missouri': 'MO', 'Northern Mariana Islands': 'MP', 
              'Mississippi': 'MS', 'Montana': 'MT', 'National': 'NA', 'North Carolina': 'NC', 
              'North Dakota': 'ND', 'Nebraska': 'NE', 'New Hampshire': 'NH', 
              'New Jersey': 'NJ', 'New Mexico': 'NM', 'Nevada': 'NV', 'New York': 'NY', 
              'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 
              'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 
              'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 
              'Virginia': 'VA', 'Virgin Islands': 'VI', 'Vermont': 'VT', 'Washington': 'WA', 
              'Wisconsin': 'WI', 'West Virginia': 'WV', 'Wyoming': 'WY'}

# Add state abbreviation column to impaired df to help with merging into location df
impaired['state_abbr'] = impaired['State'].map(state_list)    
    
# Merge lakes, rivers, estuaries info into location df
location_fac_info.rename(columns={'STATE_CODE':'state_abbr'}, inplace=True)
location_state_info = pd.merge(location_fac_info, impaired, how='left', on=['state_abbr', 'state_abbr'])
location = location_state_info

# Convert chemical_wide df to narrower, focused fact table based on individual facility & chemical info
# Keep rows with 2 or more non-NA values - this means ID and a chemical limit or something
chemical_wide = chemical_wide.dropna(thresh=2)

# Staging table as fact table design
chemical = pd.DataFrame(columns=['ID','Chemical_Name','MinLimit','MaxLimit','Units'])

try:
    for _ID in chemical_wide.ID:
        
        N = {'ID': chemical_wide.iloc[_ID]['ID'],
                   'Chemical_Name': 'N', 
                   'MinLimit': chemical_wide.iloc[_ID]['TOTAL_N_MIN_LIMIT'], 
                   'MaxLimit': chemical_wide.iloc[_ID]['TOTAL_N_MAX_LIMIT'], 
                   'Units': chemical_wide.iloc[_ID]['TOTAL_N_LIMIT_UNITS']}
        
        P = {'ID': chemical_wide.iloc[_ID]['ID'],
                   'Chemical_Name': 'P', 
                   'MinLimit': chemical_wide.iloc[_ID]['TOTAL_P_MIN_LIMIT'], 
                   'MaxLimit': chemical_wide.iloc[_ID]['TOTAL_P_MAX_LIMIT'], 
                   'Units': chemical_wide.iloc[_ID]['TOTAL_P_LIMIT_UNITS']}
        
        TKN = {'ID': chemical_wide.iloc[_ID]['ID'],
                   'Chemical_Name': 'TKN', 
                   'MinLimit': chemical_wide.iloc[_ID]['TKN_MIN_LIMIT'], 
                   'MaxLimit': chemical_wide.iloc[_ID]['TKN_MAX_LIMIT'], 
                   'Units': chemical_wide.iloc[_ID]['TKN_LIMIT_UNITS']}
        
        ORGN = {'ID': chemical_wide.iloc[_ID]['ID'],
                   'Chemical_Name': 'ORGN', 
                   'MinLimit': chemical_wide.iloc[_ID]['ORGN_MIN_LIMIT'], 
                   'MaxLimit': chemical_wide.iloc[_ID]['ORGN_MAX_LIMIT'], 
                   'Units': chemical_wide.iloc[_ID]['ORGN_LIMIT_UNITS']}
        
        AMMONIA = {'ID': chemical_wide.iloc[_ID]['ID'],
                   'Chemical_Name': 'AMMONIA', 
                   'MinLimit': chemical_wide.iloc[_ID]['AMMONIA_MIN_LIMIT'], 
                   'MaxLimit': chemical_wide.iloc[_ID]['AMMONIA_MAX_LIMIT'], 
                   'Units': chemical_wide.iloc[_ID]['AMMONIA_LIMIT_UNITS']}
        
        INORGN = {'ID': chemical_wide.iloc[_ID]['ID'],
                   'Chemical_Name': 'INORGN', 
                   'MinLimit': chemical_wide.iloc[_ID]['INORGN_MIN_LIMIT'], 
                   'MaxLimit': chemical_wide.iloc[_ID]['INORGN_MAX_LIMIT'], 
                   'Units': chemical_wide.iloc[_ID]['INORGN_LIMIT_UNITS']}
        
        NITRATE = {'ID': chemical_wide.iloc[_ID]['ID'],
                   'Chemical_Name': 'NITRATE', 
                   'MinLimit': chemical_wide.iloc[_ID]['NITRATE_MIN_LIMIT'], 
                   'MaxLimit': chemical_wide.iloc[_ID]['NITRATE_MAX_LIMIT'], 
                   'Units': chemical_wide.iloc[_ID]['NITRATE_LIMIT_UNITS']}
        
        PO4 = {'ID': chemical_wide.iloc[_ID]['ID'],
                   'Chemical_Name': 'PO4', 
                   'MinLimit': chemical_wide.iloc[_ID]['PO4_MIN_LIMIT'], 
                   'MaxLimit': chemical_wide.iloc[_ID]['PO4_MAX_LIMIT'], 
                   'Units': chemical_wide.iloc[_ID]['PO4_LIMIT_UNITS']}
        
        chemical = chemical.append(N, ignore_index=True)
        chemical = chemical.append(P, ignore_index=True)
        chemical = chemical.append(TKN, ignore_index=True)
        chemical = chemical.append(ORGN, ignore_index=True)
        chemical = chemical.append(AMMONIA, ignore_index=True)
        chemical = chemical.append(INORGN, ignore_index=True)
        chemical = chemical.append(NITRATE, ignore_index=True)
        chemical = chemical.append(PO4, ignore_index=True)

except IndexError:
    pass


date = facilities[['ID','DMR_YEAR']]
# date['datetime'] = pd.to_datetime(date[['DMR_YEAR','','']], errors='coerce')

climate = NOAA


##### EXPORT transformed dataframes
facility.to_csv(path_or_buf='C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/FACILITY.csv', index=False, encoding='utf-8')
chemical.to_csv(path_or_buf='C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/CHEMICAL.csv', index=False, encoding='utf-8')
location.to_csv(path_or_buf='C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/LOCATION.csv', index=False, encoding='utf-8')
climate.to_csv(path_or_buf='C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/LOCATION.csv', index=False, encoding='utf-8')
