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


# FacilityID = LocationID = Facility_Ref