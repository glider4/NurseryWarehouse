-- Build database

DROP TABLE IF EXISTS FACILITY;
DROP TABLE IF EXISTS CLIMATE;
DROP TABLE IF EXISTS CHEMICAL;
DROP TABLE IF EXISTS LOCATION;
DROP TABLE IF EXISTS DATE;
DROP TABLE IF EXISTS NURSERY_ANALYSIS;

CREATE TABLE FACILITY (
	Facility_ID INTEGER PRIMARY KEY NOT NULL,
	Facility_UIN INTEGER NOT NULL,
	PermitNumber INTEGER,
	PermitType VARCHAR(6),
	FacilityName VARCHAR(100),
	FacilityType VARCHAR(50),
	FacilityDetail VARCHAR(100),
	LikelyToDischargeNP VARCHAR(6),
	Has_N_Limits VARCHAR(6),
	Has_P_Limits VARCHAR(6),
	Has_N_Monitoring VARCHAR(6),
	Has_P_Monitoring VARCHAR(6),
	SICCODE INTEGER,
	NAICS_CODE INTEGER,
	Major_Minor_Flag CHAR(1),
	Design_Flow NUMERIC,
	Actual_Flow NUMERIC
);

CREATE TABLE CLIMATE (
	Climate_ID INTEGER PRIMARY KEY NOT NULL,
	State CHAR(2),
	Temperature NUMERIC,
	Humidity NUMERIC,
	AbnormalHiFlag CHAR(1),
	AbnormalLoFlag CHAR(1)
);

CREATE TABLE CHEMICAL (
	Chemical_ID INTEGER PRIMARY KEY NOT NULL,
	Chem_Name VARCHAR(50),
	Min_Limit VARCHAR(6),
	Max_Limit VARCHAR(6),
	Units VARCHAR(10)
);

CREATE TABLE LOCATION (
	Location_ID INTEGER PRIMARY KEY NOT NULL,
	City VARCHAR(50),
	State VARCHAR(50),
	Zip NUMERIC,
	County VARCHAR(50),
	EPARegion VARCHAR(50),
	Latitude NUMERIC,
	Longtitude NUMERIC,
	PrcntRiversImpaired NUMERIC,
	PrcntEstuariesImpaired NUMERIC,
	PrcntLakesImpaired NUMERIC
);

CREATE TABLE DATE (
	Date_ID INTEGER PRIMARY KEY NOT NULL,
	Year INTEGER,
	DateTime DATE
);

CREATE TABLE NURSERY_ANALYSIS (
	FACILITY_ID INTEGER,
	LOCATION_ID INTEGER,
	CLIMATE_ID INTEGER,
	CHEMICAL_ID INTEGER,
	DATE_ID INTEGER,
	Datetime DATE,
	AvgChemDischargeLimit NUMERIC,
	AvgSeasonLength NUMERIC,
	AvgDailyTemp NUMERIC,
	PrcntChemsMonitored NUMERIC,
	NumChemsDischarged NUMERIC,
	NumAbnormalLo NUMERIC,
	NumAbnormalHi NUMERIC
);
