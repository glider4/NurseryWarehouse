-- Build database

DROP TABLE IF EXISTS FACILITY;
DROP TABLE IF EXISTS CLIMATE;
DROP TABLE IF EXISTS CHEMICAL;
DROP TABLE IF EXISTS LOCATION;
DROP TABLE IF EXISTS DATE;
DROP TABLE IF EXISTS NURSERY_ANALYSIS;

CREATE TABLE FACILITY (
	Facility_ID INTEGER PRIMARY KEY NOT NULL,
	Facility_UIN NUMERIC,
	PermitNumber VARCHAR(15),
	PermitType VARCHAR(6),
	FacilityName VARCHAR(100),
	FacilityType VARCHAR(50),
	FacilityDetail VARCHAR(100),
	LikelyToDischargeNP VARCHAR(6),
	Has_N_Limits VARCHAR(6),
	Has_P_Limits VARCHAR(6),
	Has_N_Monitoring VARCHAR(6),
	Has_P_Monitoring VARCHAR(6),
	SICCODE VARCHAR(15),
	NAICS_CODE VARCHAR(15),
	Major_Minor_Flag CHAR(1),
	Design_Flow NUMERIC,
	Actual_Flow NUMERIC
);

CREATE TABLE CLIMATE (
	Climate_ID INTEGER PRIMARY KEY NOT NULL,
	State CHAR(2),
	Temperature NUMERIC,
	AbnormalHiFlag CHAR(1),
	AbnormalLoFlag CHAR(1)
);

CREATE TABLE CHEMICAL (
	Chemical_ID INTEGER PRIMARY KEY NOT NULL,
	Facility_Ref INTEGER,
	Chem_Name VARCHAR(50),
	Min_Limit VARCHAR(20),
	Max_Limit VARCHAR(20),
	Units VARCHAR(10)
);

CREATE TABLE LOCATION (
	Location_ID INTEGER PRIMARY KEY NOT NULL,
	City VARCHAR(50),
	State VARCHAR(50),
	Zip VARCHAR(15),
	County VARCHAR(50),
	EPARegion VARCHAR(50),
	Latitude NUMERIC,
	Longtitude NUMERIC,
	State_Long VARCHAR(30),
	AssessedLakesAcres NUMERIC,
	PrcntAssessedLakes VARCHAR(25), 
	LakesWithNutrientImpairAcres NUMERIC,
	PrctLakesImpaired NUMERIC,
	PrcntLakesImparedwithRestorationPlan NUMERIC,
	LakesReportYear NUMERIC, 
	AssessedRiversMi NUMERIC, 
	PrcntAssessedRivers VARCHAR(25),
	RiversWithNutrientImpairMiles NUMERIC, 
	PrctRiversImpaired NUMERIC,
	PrcntRiversImparedwithRestorationPlan NUMERIC, 
	RiversReportYear NUMERIC,
	AssessedEstuariesSqMi NUMERIC, 
	PrcntAssessedEstuaries VARCHAR(25),
	EstuariesWithNutrientImpairSqMi NUMERIC, 
	PrcntEstuariesImpaired NUMERIC,
	PrcntEstuariesImparedwithRestorationPlan NUMERIC, 
	EstuariesReportYear NUMERIC
);

CREATE TABLE DATE (
	Date_ID INTEGER PRIMARY KEY NOT NULL,
	Year INTEGER,
	Month INTEGER,
	DateTime DATE
);

CREATE TABLE NURSERY_ANALYSIS (
	FACILITY_ID INTEGER,
	LOCATION_ID INTEGER,
	CLIMATE_ID INTEGER,
	CHEMICAL_ID INTEGER,
	DATE_ID INTEGER,
	AvgChemDischargeLimit NUMERIC,
	AvgSeasonLength NUMERIC,
	AvgMonthlyTemp NUMERIC,
	PrcntChemsMonitored NUMERIC,
	NumChemsDischarged NUMERIC,
	NumAbnormalHi NUMERIC,
	NumAbnormalLo NUMERIC
);

COPY FACILITY FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/FACILITY.csv' (FORMAT CSV, DELIMITER(','), HEADER);
--COPY CLIMATE FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/CLIMATE.csv' (FORMAT CSV, DELIMITER(','), HEADER);
COPY CHEMICAL FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/CHEMICAL.csv' (FORMAT CSV, DELIMITER(','), HEADER);
COPY LOCATION FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/LOCATION.csv' (FORMAT CSV, DELIMITER(','), HEADER);
--COPY DATE FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/DATE.csv' (FORMAT CSV, DELIMITER(','), HEADER);
--COPY NURSERY_ANALYSIS FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/NURSERY_ANALYSIS.csv' (FORMAT CSV, DELIMITER(','), HEADER);

