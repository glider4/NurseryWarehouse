#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean up & transform nursery data; prepare to load into postgres database.
Create fact table structure and populate with data from cleaned datasets.
"""

import pandas as pd


# Set paths to data files
facilities_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/Facilities_Likely_NP.csv'
estuaries_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/impairedestuaries.xlsx'
rivers_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/impairedrivers.xlsx'
lakes_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/impairedlakes.xlsx'
waters_path = 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/Waters_Listed_NP_Impairments.csv'


# Import data files as DataFrames
facilities = pd.read_csv(facilities_path, delimiter=',', encoding='iso-8859-1')
estuaries = pd.read_excel(estuaries_path, skiprows=2)
rivers = pd.read_excel(rivers_path, skiprows=2)
lakes = pd.read_excel(lakes_path, skiprows=2)
waters = pd.read_csv(waters_path, delimiter=',', encoding='iso-8859-1')


# Use index of facilities to help join fact tables later on
facilities['ID'] = facilities.index


# Subset data into multiple tables
facility = facilities[['ID','UIN','EXTERNAL_PERMIT_NMBR','PERMIT_TYPE_CODE','FACILITY_NAME','FACILITY_TYPE_INDICATOR',
                       'FACILITY_DETAIL_LINK','LIKELY_TO_DISCHARGE_N_OR_P',
                       'HAS_N_LIMITS','HAS_P_LIMITS','HAS_N_MONITORING','HAS_P_MONITORING',
                       'SICCODE','NAICS_CODE','MAJOR_MINOR_STATUS_FLAG',
                       'TOTAL_DESIGN_FLOW_NMBR', 'ACTUAL_AVERAGE_FLOW_NMBR']]

location = facilities[['ID','CITY','STATE_CODE','ZIP',
                       'COUNTY_NAME','EPA_REGION_CODE',
                       'GOECODE_LATITUDE', 'GEOCODE_LONGITUDE']]

chemical_wide = facilities[['ID','TOTAL_N_MIN_LIMIT','TOTAL_N_MAX_LIMIT','TOTAL_N_LIMIT_UNITS',
                       'TKN_MIN_LIMIT','TKN_MAX_LIMIT','TKN_LIMIT_UNITS','ORGN_MIN_LIMIT',
                       'ORGN_MAX_LIMIT','ORGN_LIMIT_UNITS','AMMONIA_MIN_LIMIT',
                       'AMMONIA_MAX_LIMIT','AMMONIA_LIMIT_UNITS','INORGN_MIN_LIMIT',
                       'INORGN_MAX_LIMIT','INORGN_LIMIT_UNITS','NITRATE_MIN_LIMIT',
                       'NITRATE_MAX_LIMIT','NITRATE_LIMIT_UNITS','TOTAL_P_MIN_LIMIT',
                       'TOTAL_P_MAX_LIMIT','TOTAL_P_LIMIT_UNITS','PO4_MIN_LIMIT','PO4_MAX_LIMIT',
                       'PO4_LIMIT_UNITS']]


# Convert chemical_wide df to narrower, focused fact table based on individual facility & chemical info
chemical = pd.DataFrame(columns=['ID','Chemical_Name','MinLimit','MaxLimit','Units'])

for _ID in range(0, len(chemical_wide)-1):
    
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
    
    
date = facilities[['ID','DMR_YEAR']]
# date['datetime'] = pd.to_datetime(date[['DMR_YEAR','','']], errors='coerce')