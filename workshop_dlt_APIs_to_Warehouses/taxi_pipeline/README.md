# NYC Taxi Data Pipeline

This directory contains a dlt (data load tool) pipeline for extracting NYC taxi trip data from the Data Engineering Zoomcamp API.

## Overview

The pipeline fetches NYC taxi trip records using a custom dlt resource with page-based pagination and loads the data into DuckDB.

## Files

- `taxi_pipeline.py` - Main pipeline implementation
- `pyproject.toml` - Project dependencies (uv package manager)
- `main.py` - Basic dlt import test

## API Details

- **Base URL**: `https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api`
- **Pagination**: Page-based pagination (page parameter)
- **Termination**: Stops when an empty array `[]` is returned

## Data Schema

Each taxi trip record contains:
- `Trip_Pickup_DateTime` - Pickup timestamp
- `Trip_Dropoff_DateTime` - Dropoff timestamp  
- `Start_Lat`, `Start_Lon` - Pickup coordinates
- `End_Lat`, `End_Lon` - Dropoff coordinates
- `Trip_Distance` - Distance in miles
- `Fare_Amt` - Base fare amount
- `Tip_Amt` - Tip amount
- `Tolls_Amt` - Tolls amount
- `Total_Amt` - Total amount paid
- `Passenger_Count` - Number of passengers
- `Payment_Type` - Payment method (Cash/Credit)
- `vendor_name` - Taxi vendor (VTS/CMT)
- Additional metadata fields

## Usage

### Run full pipeline

```bash
cd /workspaces/Zoomcamp_DE_2026_Homework/workshop_dlt_APIs_to_Warehouses/taxi_pipeline
uv run python taxi_pipeline.py
```

This will:
1. Fetch all available taxi trip data page by page
2. Load it into DuckDB database
3. Create table `nyc_taxi_data.taxi_trips`

### Query the data

After running the pipeline, query the data using DuckDB:

```bash
uv run python -c "
import duckdb
conn = duckdb.connect('taxi_pipeline.duckdb')

# Show all tables
print('Tables:', conn.execute('SHOW TABLES').df())

# Count records
print('Total records:', conn.execute('SELECT COUNT(*) FROM nyc_taxi_data.taxi_trips').fetchone()[0])

# Get date range
print('Date range:')
print(conn.execute('''
    SELECT 
        MIN(\"Trip_Pickup_DateTime\") as earliest_pickup,
        MAX(\"Trip_Pickup_DateTime\") as latest_pickup
    FROM nyc_taxi_data.taxi_trips
''').df())

# Sample data
print('Sample records:')
print(conn.execute('SELECT * FROM nyc_taxi_data.taxi_trips LIMIT 5').df())
"
```

## Pipeline Implementation

The pipeline uses a custom dlt resource with manual pagination:

```python
import dlt
import requests

@dlt.resource(name="taxi_trips", write_disposition="replace")
def taxi_trips():
    base_url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
    page = 1
    
    while True:
        print(f"Fetching page {page}...")
        response = requests.get(base_url, params={"page": page})
        data = response.json()
        
        if not data:  # Stop on empty page
            print(f"Page {page} is empty, stopping! Total pages: {page-1}")
            break
        
        yield data
        page += 1

pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="nyc_taxi_data",
)

load_info = pipeline.run(taxi_trips())
```

## Dependencies

- `dlt[duckdb]>=1.17.1` - Data load tool with DuckDB support
- `requests>=2.31.0` - HTTP library for API calls

Managed by uv package manager (automatic installation on first run).

## MCP Integration

The parent directory contains `mcp.json` configuration to enable the dlt MCP server, providing:
- Access to dlt documentation
- Code examples and patterns  
- Pipeline metadata inspection

## Troubleshooting

### Pipeline not loading data

Check if the API is accessible:
```bash
curl "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api?page=1"
```

### Database file not found

The database file `taxi_pipeline.duckdb` is created in the current directory when the pipeline runs.

### View pipeline information

```bash
uv run dlt pipeline taxi_pipeline info
```

