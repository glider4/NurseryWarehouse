-- Export data for CLIMATE fact table: average monthly temps for NOAA GHCN-D US locations

COPY (

	WITH main_CTE AS
	(
	SELECT stationid, stateabbr, month, year, v1,v2,v3,v4,v5,v6,v7,v8,
			v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21,v22,v23,v24,v25,v26,v27,v28,v29,v30,v31
	FROM OBS
	INNER JOIN Stations USING(StationID)
	WHERE Element IN('TAVG')
		AND CountryAbbr = 'US'
		AND Year IN(2008, 2009, 2010, 2011, 2012)
	),


	average_CTE AS 
	(

	(
	-- 31 day months
	SELECT stateabbr, stationid, month, year,
		((v1+v2+v3+v4+v5+v6+v7+v8+v9+v10+v11+v12+v13+v14+v15+v16+v17+
		  v18+v19+v20+v21+v22+v23+v24+v25+v26+v27+v28+v29+v30+v31)/31) AS month_avg
	FROM main_CTE
	WHERE month IN(1,3,5,7,8,10,12)
		AND ((v1+v2+v3+v4+v5+v6+v7+v8+v9+v10+v11+v12+v13+v14+v15+v16+v17+
			  v18+v19+v20+v21+v22+v23+v24+v25+v26+v27+v28+v29+v30+v31)/31) IS NOT NULL
	)

	UNION ALL

	(
	-- 30 day months
	SELECT stateabbr, stationid, month, year,
		((v1+v2+v3+v4+v5+v6+v7+v8+v9+v10+v11+v12+v13+v14+v15+v16+v17+
		  v18+v19+v20+v21+v22+v23+v24+v25+v26+v27+v28+v29+v30)/30) AS month_avg
	FROM main_CTE
	WHERE month IN(4,6,9,11)
		AND ((v1+v2+v3+v4+v5+v6+v7+v8+v9+v10+v11+v12+v13+v14+v15+v16+v17+
			  v18+v19+v20+v21+v22+v23+v24+v25+v26+v27+v28+v29+v30)/30) IS NOT NULL
	)

	UNION ALL

	(
	-- February, 28 days, NOT leap years
	SELECT stateabbr, stationid, month, year,
		((v1+v2+v3+v4+v5+v6+v7+v8+v9+v10+v11+v12+v13+v14+v15+v16+v17+
		  v18+v19+v20+v21+v22+v23+v24+v25+v26+v27+v28)/28) AS month_avg
	FROM main_CTE
	WHERE month IN(2)
		AND ((v1+v2+v3+v4+v5+v6+v7+v8+v9+v10+v11+v12+v13+v14+v15+v16+v17+
			  v18+v19+v20+v21+v22+v23+v24+v25+v26+v27+v28)/28) IS NOT NULL
		AND (year%4) != 0
	)

	UNION ALL

	(
	-- February, 29 days, leap years
	SELECT stateabbr, stationid, month, year,
		((v1+v2+v3+v4+v5+v6+v7+v8+v9+v10+v11+v12+v13+v14+v15+v16+v17+
		  v18+v19+v20+v21+v22+v23+v24+v25+v26+v27+v28+v29)/29) AS month_avg
	FROM main_CTE
	WHERE month IN(2)
		AND ((v1+v2+v3+v4+v5+v6+v7+v8+v9+v10+v11+v12+v13+v14+v15+v16+v17+
			  v18+v19+v20+v21+v22+v23+v24+v25+v26+v27+v28+v29)/29) IS NOT NULL
		AND (year%4) = 0
		AND (year%100) = 0
		AND (year%400) = 0
	)

	)

	-- Averages per month
	SELECT stateabbr, month, year, AVG(month_avg)/10 AS average_monthly_C
	FROM average_CTE
	GROUP BY stateabbr, month, year
	ORDER BY stateabbr, month, year

) 
TO 'C:\Users\dell\Documents\GitHub\NurseryWarehouse\data\raw_data\NOAA_GHCND_subset.csv'
WITH (FORMAT CSV, HEADER);
