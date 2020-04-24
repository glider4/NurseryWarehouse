-- Build database

DROP TABLE IF EXISTS FACILITY CASCADE;
DROP TABLE IF EXISTS CLIMATE CASCADE;
DROP TABLE IF EXISTS CHEMICAL CASCADE;
DROP TABLE IF EXISTS LOCATION CASCADE;
DROP TABLE IF EXISTS DATE CASCADE;
DROP TABLE IF EXISTS NURSERY_ANALYSIS CASCADE;

CREATE TABLE FACILITY (
	Facility_ID NUMERIC PRIMARY KEY NOT NULL,
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
	Climate_ID NUMERIC PRIMARY KEY NOT NULL,
	State CHAR(2),
	Month VARCHAR(20),
	Year INTEGER,
	AvgTempC NUMERIC,
	AbnormalHiFlag CHAR(1),
	AbnormalLoFlag CHAR(1)
);

CREATE TABLE CHEMICAL (
	Chemical_ID NUMERIC PRIMARY KEY NOT NULL,
	Facility_Ref INTEGER,
	Chem_Name VARCHAR(50),
	Min_Limit VARCHAR(20),
	Max_Limit VARCHAR(20),
	Units VARCHAR(10)
);

CREATE TABLE LOCATION (
	Location_ID NUMERIC PRIMARY KEY NOT NULL,
	City VARCHAR(50),
	State VARCHAR(50),
	Zip VARCHAR(15),
	County VARCHAR(50),
	EPARegion VARCHAR(50),
	Latitude NUMERIC,
	Longtitude NUMERIC,
	State_Long VARCHAR(30),
	AssessedLakesAcres NUMERIC,
	PrctAssessedLakes VARCHAR(25), 
	LakesImpairedAcres NUMERIC,
	PrctLakesImpaired NUMERIC,
	PrctLakesRestoration NUMERIC,
	LakesReportYear NUMERIC, 
	AssessedRiversMiles NUMERIC, 
	PrctAssessedRivers VARCHAR(25),
	RiversImpairedMiles NUMERIC, 
	PrctRiversImpaired NUMERIC,
	PrctRiversRestoration NUMERIC, 
	RiversReportYear NUMERIC,
	AssessedEstuariesSqMi NUMERIC, 
	PrctAssessedEstuaries VARCHAR(25),
	EstuariesImpairedSqMi NUMERIC, 
	PrctEstuariesImpaired NUMERIC,
	PrctEstuariesRestoration NUMERIC, 
	EstuariesReportYear NUMERIC
);

CREATE TABLE DATE (
	Date_ID INTEGER PRIMARY KEY NOT NULL,
	Datetime DATE,
	YearMonthNum INTEGER,
	MonthNum INTEGER,
	MonthName VARCHAR(20),
	MonthShortName VARCHAR(5),
	WeekNum INTEGER,
	DayNumofYear INTEGER,
	DayNumofMonth INTEGER,
	DayNumofWeek INTEGER,
	DayName VARCHAR(10),
	DayShortName VARCHAR(4),
	Quarter INTEGER,
	DayNumofQuarter INTEGER
);

CREATE TABLE NURSERY_ANALYSIS (
	FACILITY_ID NUMERIC,
	LOCATION_ID NUMERIC,
	CLIMATE_ID NUMERIC,
	CHEMICAL_ID NUMERIC,
	DATE_ID NUMERIC,
	AvgChemDischargeLimit NUMERIC,
	AvgSeasonLength NUMERIC,
	AvgMonthlyTemp NUMERIC,
	PrcntChemsMonitored NUMERIC,
	NumChemsDischarged NUMERIC,
	NumAbnormalHi NUMERIC,
	NumAbnormalLo NUMERIC
);

COPY FACILITY FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/FACILITY.csv' (FORMAT CSV, DELIMITER(','), HEADER);
COPY CLIMATE FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/CLIMATE.csv' (FORMAT CSV, DELIMITER(','), HEADER);
COPY CHEMICAL FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/CHEMICAL.csv' (FORMAT CSV, DELIMITER(','), HEADER);
COPY LOCATION FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/LOCATION.csv' (FORMAT CSV, DELIMITER(','), HEADER);
COPY DATE FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/DATE.csv' (FORMAT CSV, DELIMITER(','), HEADER);
COPY NURSERY_ANALYSIS FROM 'C:/Users/dell/Documents/GitHub/NurseryWarehouse/data/transformed_data/NURSERY_ANALYSIS.csv' (FORMAT CSV, DELIMITER(','), HEADER);

SELECT * FROM NURSERY_ANALYSIS
ORDER BY avgseasonlength DESC;