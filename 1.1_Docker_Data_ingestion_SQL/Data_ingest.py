#!/usr/bin/env python
# coding: utf-8
"""
Data Ingestion Script for NYC Taxi Data

This script ingests taxi zone and green taxi trip data into PostgreSQL database.
It handles data type conversion, validation, and chunked insertion for large datasets.
"""

# ============================================================================
# IMPORTS AND DEPENDENCIES
# ============================================================================

import pandas as pd
from sqlalchemy import create_engine
import dask.dataframe as dd
import click
import sys

# Note: Dependencies should be installed via:
# uv add dask[complete] aiohttp requests pyarrow fastparquet sqlalchemy psycopg2-binary click


# ============================================================================
# SECTION 1: TAXI ZONE DATA INGESTION
# ============================================================================

def load_and_ingest_taxi_zones(engine):
    """
    Load taxi zone lookup data from CSV and ingest into PostgreSQL.
    
    - Downloads zone lookup data from GitHub releases
    - Converts data types for consistency
    - Creates table schema in database
    - Inserts all records
    
    Args:
        engine: SQLAlchemy database connection engine
    """
    
    # Source URL for taxi zone lookup data
    url_1 = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'
    
    # Define data types for taxi zone columns
    dtype_zones = {
        "LocationID": "int32",       # Join key for location identifier
        "Borough": "string",          # NYC borough name
        "Zone": "string",             # Zone name
        "service_zone": "string"      # Service zone type
    }
    
    # Read CSV with proper data types
    df = pd.read_csv(url_1, dtype=dtype_zones)
    print("\n=== TAXI ZONE DATA ===")
    print(f"Shape: {df.shape}")
    print(f"Data Types:\n{df.dtypes}")
    
    # Display the schema that will be created in the database
    print(f"\nTable Schema:\n{pd.io.sql.get_schema(df, name='taxi_zone', con=engine)}")
    
    # Create empty table in PostgreSQL (replaces if exists)
    df.head(n=0).to_sql(name='taxi_zone', con=engine, if_exists='replace')
    
    # Insert all data into the table
    df.to_sql(name='taxi_zone', con=engine, if_exists='append')
    print(f"\n✓ Inserted {len(df)} taxi zone records into 'taxi_zone' table")
    
    return engine


# ============================================================================
# SECTION 2: GREEN TAXI TRIP DATA INGESTION
# ============================================================================

def load_and_prepare_green_taxi_data(url_2):
    """
    Load green taxi trip data from Parquet file and prepare for database insertion.
    
    - Reads Parquet file from remote source
    - Converts data types for proper database storage
    - Converts datetime columns to proper format
    - Returns prepared DataFrame
    """
    
    # Read Parquet file
    df = pd.read_parquet(url_2)
    print("\n=== GREEN TAXI TRIP DATA ===")
    print(f"Initial Shape: {df.shape}")
    print(f"Initial Columns: {df.columns.tolist()}")
    
    # Define data types for trip columns
    dtype_trips = {
        # Categorical/ID columns
        "VendorID": "Int32",
        "store_and_fwd_flag": "string",
        "RatecodeID": "Int32",
        "PULocationID": "Int32",        # Pickup location ID
        "DOLocationID": "Int32",        # Dropoff location ID
        "passenger_count": "Int32",
        "payment_type": "Int32",
        "trip_type": "Int32",
        
        # Continuous/monetary columns
        "trip_distance": "float64",
        "fare_amount": "float64",
        "extra": "float64",             # Miscellaneous extras
        "mta_tax": "float64",           # MTA tax
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "ehail_fee": "float64",         # E-hail fee
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64",
        "cbd_congestion_fee": "float64"
    }
    
    # Convert data types
    df = df.astype(dtype_trips)
    print(f"\nData types converted successfully")
    
    # Convert datetime columns to proper format
    parse_dates = ["lpep_pickup_datetime", "lpep_dropoff_datetime"]
    for col in parse_dates:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    
    print(f"Datetime columns converted")
    print(f"Final Data Types:\n{df.dtypes}")
    
    return df


def ingest_with_dask(url_2, engine):
    """
    Read Parquet file using Dask and insert data into PostgreSQL in chunks.
    
    - Uses Dask for memory-efficient processing of large files
    - Processes each partition separately
    - Inserts each partition into the database
    """
    
    # Create Dask DataFrame for chunked processing
    ddf = dd.read_parquet(url_2)
    
    print(f"\nTotal partitions: {ddf.npartitions}")
    
    # Process and insert each partition separately
    for i in range(ddf.npartitions):
        partition = ddf.get_partition(i).compute()
        
        # Prepare data types (same as main dataset)
        dtype_trips = {
            "VendorID": "Int32",
            "store_and_fwd_flag": "string",
            "RatecodeID": "Int32",
            "PULocationID": "Int32",
            "DOLocationID": "Int32",
            "passenger_count": "Int32",
            "payment_type": "Int32",
            "trip_type": "Int32",
            "trip_distance": "float64",
            "fare_amount": "float64",
            "extra": "float64",
            "mta_tax": "float64",
            "tip_amount": "float64",
            "tolls_amount": "float64",
            "ehail_fee": "float64",
            "improvement_surcharge": "float64",
            "total_amount": "float64",
            "congestion_surcharge": "float64",
            "cbd_congestion_fee": "float64",
        }
        
        partition = partition.astype(dtype_trips)
        
        # Convert datetime columns
        parse_dates = ["lpep_pickup_datetime", "lpep_dropoff_datetime"]
        for col in parse_dates:
            if col in partition.columns:
                partition[col] = pd.to_datetime(partition[col])
        
        # Insert partition into database
        partition.to_sql('green_taxi_data', con=engine, if_exists='append', index=False)
        print(f'✓ Inserted partition {i} (shape: {partition.shape})')


# ============================================================================
# MAIN EXECUTION WITH CLICK CLI
# ============================================================================

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host address')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port number')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--zone-table', default='taxi_zone', help='Table name for taxi zones')
@click.option('--trip-table', default='green_taxi_data', help='Table name for trip data')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, zone_table, trip_table):
    """
    Ingest NYC taxi data into PostgreSQL database.
    
    This script downloads taxi zone and green taxi trip data,
    converts data types, and inserts them into PostgreSQL.
    
    Example usage:
        python Data_ingest.py --pg-user root --pg-pass root
        python Data_ingest.py --pg-host 192.168.1.100 --pg-db production_db
    """
    
    try:
        # Build PostgreSQL connection string from CLI parameters
        connection_string = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
        engine = create_engine(connection_string)
        
        print(f"\n{'='*70}")
        print(f"DATABASE CONNECTION: {pg_host}:{pg_port}/{pg_db}")
        print(f"{'='*70}")
        
        # Step 1: Ingest taxi zone data
        print("\n[STEP 1] Ingesting taxi zone data...")
        load_and_ingest_taxi_zones(engine)
        
        # Step 2: Load and prepare green taxi data
        url_2 = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
        print(f"\n[STEP 2] Loading green taxi trip data from: {url_2}")
        df = load_and_prepare_green_taxi_data(url_2)
        
        # Create empty table in PostgreSQL
        print(f"\nTable Schema for {trip_table}:")
        print(pd.io.sql.get_schema(df, name=trip_table, con=engine))
        df.head(n=0).to_sql(name=trip_table, con=engine, if_exists='replace')
        
        # Step 3: Ingest data using Dask for chunked processing
        print(f"\n[STEP 3] Starting chunked data ingestion...")
        ingest_with_dask(url_2, engine)
        
        print(f"\n{'='*70}")
        print("✓ DATA INGESTION COMPLETE")
        print(f"{'='*70}")
        print(f"Successfully created and populated:")
        print(f"  • Table: {zone_table}")
        print(f"  • Table: {trip_table}")
        print(f"\nDatabase: {pg_db} @ {pg_host}:{pg_port}")
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print(f"Could not connect to PostgreSQL database at {pg_host}:{pg_port}")
        raise


if __name__ == "__main__":
    run()




