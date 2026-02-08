-- Homework Week 3: BigQuery Data Warehousing
-- Project ID: zeta-medley-473321-r6
-- Dataset Location: EU

-- 1. Create an External Table pointing to the GCS Bucket
-- Note: Ensure the dataset location matches the bucket location (EU)
CREATE OR REPLACE EXTERNAL TABLE `zeta-medley-473321-r6.homework_w3_eu.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://2026_zoomcamp_de_w3_data_warehouse_bigquery_hw/yellow_tripdata_2024-*.parquet']
);

-- 2. Create a Regular (Native) Table from the External Table
-- This imports the data into BigQuery's internal storage
CREATE OR REPLACE TABLE `zeta-medley-473321-r6.homework_w3_eu.yellow_taxi_non_partitioned` AS
SELECT * FROM `zeta-medley-473321-r6.homework_w3_eu.external_yellow_tripdata`;

-- 0 MB for the External Table and 155.12 MB for the Materialized Table

-- 3. Compare Count Operations (Checking metadata vs. scanning)
-- Count distinct PULocationID from Native Table
SELECT COUNT(DISTINCT PULocationID) FROM `zeta-medley-473321-r6.homework_w3_eu.yellow_taxi_non_partitioned`;

-- Count distinct PULocationID from External Table
SELECT COUNT(DISTINCT PULocationID) FROM `zeta-medley-473321-r6.homework_w3_eu.external_yellow_tripdata`;

-- 4. Compare Scanning Costs (Columnar Storage behavior)
-- Retrieve a single column (PULocationID)
SELECT PULocationID FROM `zeta-medley-473321-r6.homework_w3_eu.yellow_taxi_non_partitioned`;

-- Retrieve two columns (PULocationID, DOLocationID) to see doubled scan size
SELECT PULocationID, DOLocationID FROM `zeta-medley-473321-r6.homework_w3_eu.yellow_taxi_non_partitioned`;

-- 5. Filtering zero fare trips
SELECT COUNT(*)
FROM `zeta-medley-473321-r6.homework_w3_eu.yellow_taxi_non_partitioned`
WHERE fare_amount = 0;
-- 8333	

-- 6. Create an Optimized Table (Partitioning and Clustering)
-- Strategy: Partition by dropoff date and Cluster by VendorID for optimized filtering
CREATE OR REPLACE TABLE `zeta-medley-473321-r6.homework_w3_eu.yellow_taxi_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS 
SELECT * FROM `zeta-medley-473321-r6.homework_w3_eu.external_yellow_tripdata`;

-- 7. Performance Testing: Optimized vs. Non-Partitioned
-- Query on Optimized Table (Estimated scan: ~26.84 MB)
SELECT DISTINCT(VendorID)
FROM `zeta-medley-473321-r6.homework_w3_eu.yellow_taxi_optimized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- Query on Non-Partitioned Table (Estimated scan: ~310.21 MB)
SELECT DISTINCT(VendorID)
FROM `zeta-medley-473321-r6.homework_w3_eu.yellow_taxi_non_partitioned`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';