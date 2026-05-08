# Future Integration: Snowflake Postcode Data

## What the Snowflake Integration Enables

Broadlab stores an audience graph in Snowflake covering 1.8 million UK postcodes with thousands of attributes per postcode. This data maps motivational states, demographic profiles, and behavioural signals to specific UK postcodes — the same postcode level at which addressable TV campaigns are targeted.

When this integration is complete, the Creative Intelligence Platform will move from producing audience segment recommendations to producing **specific UK postcode targeting lists**.

Current output: "Concentrate budget on young competitive males aged 18–34 with achievement motivation."

Future output: "Concentrate budget on postcodes M1, M2, LS1, LS2, B1, B2 [full list] — these 94,000 postcodes have the highest concentration of the identified target persona."

## Where to Insert the Query

Add **Step 9** to the pipeline, after `synthesis_call.py`:

```
Step 8 — synthesis_call.py        [existing — produces final report]
Step 9 — query_snowflake.py       [ADD THIS — appends postcode data to report]
```

## New File: backend/pipeline/query_snowflake.py

When implementing, this file should:

1. Read the `targeting_recommendation` section from `report.json`
2. Extract the identified top persona(s) and their motivational profile
3. Connect to Snowflake using the Snowflake Python connector with credentials from `.env`
4. Query the postcode audience table to find postcodes where the target persona has the highest index
5. Return the top postcode clusters ranked by persona concentration
6. Append these as a `postcode_recommendations` section in `report.json`

## Required .env Variables to Add

```
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=your_database_name
SNOWFLAKE_SCHEMA=your_schema_name
SNOWFLAKE_WAREHOUSE=your_warehouse_name
SNOWFLAKE_TABLE=your_postcode_audience_table
```

## Frontend Update Required

Update the Targeting Recommendation tab in `Results.jsx` to display:
- A list of recommended postcode clusters
- An estimated reach figure (number of households per cluster)
- A map visualisation of the recommended postcodes (optional enhancement)

## Required Information from Broadlab Data Team

To complete this integration, the following is needed:
1. Snowflake account credentials and connection details
2. The name and schema of the postcode audience table
3. The column names for: postcode, persona/motivation attributes, household count
4. Any query access restrictions or data governance requirements

## Contact

Snowflake credentials and table schema should be requested from the Broadlab data engineering team.
