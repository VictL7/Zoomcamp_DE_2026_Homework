"""@bruin

# TODO: Set the asset name (recommended pattern: schema.asset_name).
# - Convention in this module: use an `ingestion.` schema for raw ingestion tables.
name: ingestion.trips

# TODO: Set the asset type.
# Docs: https://getbruin.com/docs/bruin/assets/python
type: python

# TODO: Pick a Python image version (Bruin runs Python in isolated environments).
# Example: python:3.11
image: python:3.11

# TODO: Set the connection.
connection: duckdb-default

# TODO: Choose materialization (optional, but recommended).
# Bruin feature: Python materialization lets you return a DataFrame (or list[dict]) and Bruin loads it into your destination.
# This is usually the easiest way to build ingestion assets in Bruin.
# Alternative (advanced): you can skip Bruin Python materialization and write a "plain" Python asset that manually writes
# into DuckDB (or another destination) using your own client library and SQL. In that case:
# - you typically omit the `materialization:` block
# - you do NOT need a `materialize()` function; you just run Python code
# Docs: https://getbruin.com/docs/bruin/assets/python#materialization
materialization:
  # TODO: choose `table` or `view` (ingestion generally should be a table)
  type: table
  # TODO: pick a strategy.
  # suggested strategy: append
  strategy: append

# TODO: Define output columns (names + types) for metadata, lineage, and quality checks.
# Tip: mark stable identifiers as `primary_key: true` if you plan to use `merge` later.
# Docs: https://getbruin.com/docs/bruin/assets/columns
columns:
  - name: pickup_datetime
    type: timestamp
    description: The timestamp when the trip started.
  - name: dropoff_datetime
    type: timestamp
    description: The timestamp when the trip ended.
  - name: trip_distance
    type: double
    description: The distance of the trip in miles.
  - name: fare_amount
    type: double
    description: The fare amount for the trip.
  - name: taxi_type
    type: string
    description: The type of taxi (yellow or green).
  - name: payment_type
    type: integer
    description: The payment type code (1-4).

@bruin"""

# TODO: Add imports needed for your ingestion (e.g., pandas, requests).
# - Put dependencies in the nearest `requirements.txt` (this template has one at the pipeline root).
# Docs: https://getbruin.com/docs/bruin/assets/python
import os 
import json
import pandas as pd
from datetime import datetime
from dateutil.rrule import rrule, MONTHLY

# TODO: Only implement `materialize()` if you are using Bruin Python materialization.
# If you choose the manual-write approach (no `materialization:` block), remove this function and implement ingestion
# as a standard Python script instead.
def materialize():
    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]
    taxi_types = json.loads(os.environ["BRUIN_VARS"]).get("taxi_types", ["yellow"])

    # Parse dates for month generation
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Generate list of months between start and end dates
    months = [dt.strftime("%Y-%m") for dt in rrule(MONTHLY, dtstart=start_dt, until=end_dt)]
    
    # Fetch parquet files and combine
    dataframes = []
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    
    for taxi_type in taxi_types:
        for month in months:
            year, month_num = month.split("-")
            url = f"{base_url}/{taxi_type}_tripdata_{year}-{month_num}.parquet"
            
            try:
                df = pd.read_parquet(url)
                
                # Standardize column names across yellow and green taxis
                column_mapping = {
                    'tpep_pickup_datetime': 'pickup_datetime',      # Yellow taxi
                    'lpep_pickup_datetime': 'pickup_datetime',      # Green taxi
                    'tpep_dropoff_datetime': 'dropoff_datetime',    # Yellow taxi
                    'lpep_dropoff_datetime': 'dropoff_datetime',    # Green taxi
                    'PULocationID': 'pickup_location_id',
                    'DOLocationID': 'dropoff_location_id',
                    'trip_distance': 'trip_distance',
                    'fare_amount': 'fare_amount',
                    'payment_type': 'payment_type',
                }
                
                df = df.rename(columns=column_mapping)
                # Add taxi_type column for reference
                df["taxi_type"] = taxi_type
                dataframes.append(df)
                print(f"✅ Loaded {url}")
            except Exception as e:
                print(f"⚠️ Failed to load {url}: {e}")
    
    # Combine all dataframes
    if dataframes:
        final_dataframe = pd.concat(dataframes, ignore_index=True)
        # Select columns for the ingestion table
        cols_to_keep = ["pickup_datetime", "dropoff_datetime", "trip_distance", "fare_amount", "payment_type", "taxi_type"]
        available_cols = [col for col in cols_to_keep if col in final_dataframe.columns]
        final_dataframe = final_dataframe[available_cols]
    else:
        # Return empty dataframe if no data was loaded
        final_dataframe = pd.DataFrame(columns=["pickup_datetime", "dropoff_datetime", "trip_distance", "fare_amount", "payment_type", "taxi_type"])
    
    return final_dataframe


