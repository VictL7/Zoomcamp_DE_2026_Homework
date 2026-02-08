# Week 3: BigQuery Data Warehousing

This directory contains the homework for Week 3 of the Data Engineering Zoomcamp 2026.

## 🏗️ Project Overview
The goal is to orchestrate a data pipeline that loads NYC Yellow Taxi data (2024) into Google Cloud Storage (GCS) and performs analytical queries in BigQuery.

## 🚀 Key Tasks Accomplished
- **Data Ingestion**: Python script to upload 6 months of Parquet files to GCS.
- **External Tables**: Created an external table in BigQuery to query data directly from GCS.
- **Native Tables**: Materialized data into BigQuery native storage for better performance.
- **Optimization**: Implemented **Partitioning** (by `tpep_dropoff_datetime`) and **Clustering** (by `VendorID`).

## 🛠️ Tech Stack
- **Storage**: Google Cloud Storage (EU Multi-region)
- **Warehouse**: Google BigQuery
- **Language**: SQL & Python