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

# Subset data into fact tables
facility = facilities[['ID','UIN','EXTERNAL_PERMIT_NMBR','PERMIT_TYPE_CODE','FACILITY_NAME','FACILITY_TYPE_INDICATOR',
                       'FACILITY_DETAIL_LINK','LIKELY_TO_DISCHARGE_N_OR_P',
                       'HAS_N_LIMITS','HAS_P_LIMITS','HAS_N_MONITORING','HAS_P_MONITORING',
                       'SICCODE','NAICS_CODE','MAJOR_MINOR_STATUS_FLAG',
                       'TOTAL_DESIGN_FLOW_NMBR', 'ACTUAL_AVERAGE_FLOW_NMBR']]

location = facilities[['ID','CITY','STATE_CODE','ZIP',
                       'COUNTY_NAME','EPA_REGION_CODE',
                       'GOECODE_LATITUDE', 'GEOCODE_LONGITUDE']]

chemical = facilities[['ID','TOTAL_N_MIN_LIMIT','TOTAL_N_MAX_LIMIT','TOTAL_N_LIMIT_UNITS',
                       'TKN_MIN_LIMIT','TKN_MAX_LIMIT','TKN_LIMIT_UNITS','ORGN_MIN_LIMIT',
                       'ORGN_MAX_LIMIT','ORGN_LIMIT_UNITS','AMMONIA_MIN_LIMIT',
                       'AMMONIA_MAX_LIMIT','AMMONIA_LIMIT_UNITS','INORGN_MIN_LIMIT',
                       'INORGN_MAX_LIMIT','INORGN_LIMIT_UNITS','NITRATE_MIN_LIMIT',
                       'NITRATE_MAX_LIMIT','NITRATE_LIMIT_UNITS','NITRITE_MIN_LIMIT',
                       'NITRITE_MAX_LIMIT','NITRITE_LIMIT_UNITS','TOTAL_P_MIN_LIMIT',
                       'TOTAL_P_MAX_LIMIT','TOTAL_P_LIMIT_UNITS','PO4_MIN_LIMIT','PO4_MAX_LIMIT',
                       'PO4_LIMIT_UNITS']]

date = facilities[['ID','DMR_YEAR']]
date['datetime'] = pd.to_datetime(date[['DMR_YEAR','','']], errors='coerce')