# UV + dlt + MCP Integration Guide

This project demonstrates how to integrate UV (Python package manager), dlt (data load tool), and MCP (Model Context Protocol).

## Project Structure

```
workshop_dlt_APIs_to_Warehouses/
├── mcp.json                    # MCP server configuration
└── taxi_pipeline/
    ├── pyproject.toml          # UV project dependencies
    ├── taxi_pipeline.py        # Main pipeline code
    ├── main.py                 # Basic import test
    └── README.md               # Project documentation
```

## Component Overview

### 1. UV (Python Package Manager)

UV is a fast Python package manager and project management tool.

**Configuration file**: `taxi_pipeline/pyproject.toml`
```toml
[project]
name = "taxi-pipeline"
version = "0.1.0"
description = "NYC Taxi data pipeline using dlt"
requires-python = ">=3.11"
dependencies = [
  "dlt[duckdb]>=1.17.1",
  "requests>=2.31.0",
]
```

**Usage**:
```bash
# Run Python scripts (automatically manages virtual environment and dependencies)
uv run python taxi_pipeline.py
```

### 2. dlt (Data Load Tool)

dlt is a Python library for building data pipelines, supporting data extraction from various sources and loading into target databases.

**Key Features**:
- Custom dlt resources with full control
- Manual pagination handling
- Built-in support for multiple databases (DuckDB, PostgreSQL, BigQuery, etc.)
- Automatic schema inference and evolution

**Example Configuration** (from `taxi_pipeline.py`):
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

### 3. MCP (Model Context Protocol)

MCP allows AI assistants to access external tools and data sources. The dlt MCP server provides access to dlt documentation, code examples, and pipeline metadata.

**Configuration file**: `mcp.json`
```json
{
  "servers": {
    "dlt": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--with",
        "dlt[duckdb]",
        "--with",
        "dlt-mcp[search]",
        "python",
        "-m",
        "dlt_mcp"
      ]
    }
  },
  "inputs": []
}
```

**Capabilities**:
- Search dlt documentation
- Get code examples
- Inspect pipeline state and metadata
- Query schema of loaded data

## Quick Start

### 1. Test Basic Setup

```bash
cd /workspaces/Zoomcamp_DE_2026_Homework/workshop_dlt_APIs_to_Warehouses/taxi_pipeline

# Test dlt import
uv run python main.py
```

Expected output:
```
dlt version: 1.22.2
rest_api_source loaded: True
islice sample: [0, 1, 2]
```

### 2. Run Test Pipeline

```bash
# Run the full pipeline
uv run python taxi_pipeline.py
```

Expected output:
```
🚕 Starting NYC Taxi data load...
Fetching page 1...
Fetching page 2...
...
Page N is empty, stopping! Total pages: N-1
Pipeline taxi_pipeline load step completed in X.XX seconds
1 load package(s) were loaded to destination duckdb and into dataset nyc_taxi_data
✅ Complete!
```

### 3. Query the Data

```bash
# Query the loaded data
uv run python -c "
import duckdb
conn = duckdb.connect('taxi_pipeline.duckdb')

# Show tables
print('Tables:', conn.execute('SHOW TABLES').df())

# Count records
print('Total records:', conn.execute('SELECT COUNT(*) FROM nyc_taxi_data.taxi_trips').fetchone()[0])

# Get date range
print(conn.execute('''
    SELECT 
        MIN(\\\"Trip_Pickup_DateTime\\\") as earliest,
        MAX(\\\"Trip_Pickup_DateTime\\\") as latest
    FROM nyc_taxi_data.taxi_trips
''').df())
"
```

This will:
1. Connect to the DuckDB database
2. Show all tables
3. Display record count
4. Show the date range of the dataset

## API Details

**Endpoint**: `https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api`

**Pagination Parameters**:
- `page`: Page number (starts from 1)

**Response Format**: JSON array
```json
[
  {
    "Trip_Pickup_DateTime": "2009-06-14 23:23:00",
    "Trip_Dropoff_DateTime": "2009-06-14 23:48:00",
    "Start_Lat": 40.641525,
    "Start_Lon": -73.787442,
    "End_Lat": 40.742963,
    "End_Lon": -73.980072,
    "Trip_Distance": 17.52,
    "Fare_Amt": 45.0,
    "Tip_Amt": 9.0,
    "Total_Amt": 58.15,
    "Passenger_Count": 1,
    "Payment_Type": "Credit",
    "vendor_name": "VTS"
  }
]
```

**Termination Condition**: Stops when the API returns an empty array `[]`

## Pagination Strategy

The pipeline uses manual page-based pagination:

- ✅ Starts from page 1
- ✅ Increments page number after each successful request
- ✅ Detects empty pages and stops
- ✅ Uses requests library for HTTP calls

Implementation:
```python
@dlt.resource(name="taxi_trips", write_disposition="replace")
def taxi_trips():
    base_url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
    page = 1
    
    while True:
        response = requests.get(base_url, params={"page": page})
        data = response.json()
        
        if not data:  # Stop on empty page
            break
        
        yield data
        page += 1
```

## Data Flow

```
API Endpoint
   ↓ (page=1, page=2, ...)
Custom dlt Resource
   ↓ (manual pagination)
dlt Pipeline
   ↓ (schema inference)
DuckDB Database
   ↓
nyc_taxi_data.taxi_trips table
```

## Troubleshooting

### UV command not found
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### dlt import errors
```bash
# Clean and reinstall dependencies
cd taxi_pipeline
rm -rf .venv
uv run python main.py
```

### MCP server not starting
Ensure `mcp.json` is configured correctly and that VS Code or Claude Desktop is configured to use this file.

## Advanced Features

### Add Data Transformations
```python
@dlt.transformer
def clean_taxi_data(record):
    # Clean and transform data
    if record.get('Trip_Distance', 0) > 0:
        record['fare_per_mile'] = record['Fare_Amt'] / record['Trip_Distance']
    return record

# Apply transformation
pipeline.run(taxi_trips() | clean_taxi_data)
```

### Change Target Database
```python
pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="bigquery",  # or "postgres", "snowflake", etc.
    dataset_name="nyc_taxi_data",
)
```

### Incremental Loading
```python
@dlt.resource(name="taxi_trips", write_disposition="merge", primary_key="id")
def taxi_trips():
    # Use merge mode to update existing records
    # and add new ones
    ...
```

## Related Resources

- [dlt Documentation](https://dlthub.com/docs)
- [dlt REST API Source](https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api)
- [UV Documentation](https://docs.astral.sh/uv/)
- [MCP Specification](https://modelcontextprotocol.io/)

## Summary

This project demonstrates the integration of modern data engineering tools:

1. **UV** - Fast, reliable Python package management
2. **dlt** - Declarative data pipelines with minimal boilerplate
3. **MCP** - AI-assisted development with access to documentation and tools

Using these tools together enables efficient building, testing, and maintenance of data pipelines.
