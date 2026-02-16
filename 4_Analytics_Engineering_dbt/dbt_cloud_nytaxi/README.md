This project focuses on building a robust data warehouse for New York City Taxi & Limousine Commission (TLC) data using **dbt (data build tool)** and **Google BigQuery**.

## 🚀 Project Overview
The pipeline transforms raw Green and Yellow taxi trip data into clean, modeled tables. It follows the Medallion Architecture (Staging -> Core -> Marts) to enable monthly revenue analysis and business reporting.

## 🛠 Data Architecture
- **Staging Layer**: Initial cleaning, field renaming (e.g., `vendorid` to `vendor_id`), and type casting.
- **Core Layer**: Unioning different taxi types and joining with the `dim_zones` dimension table.
- **Marts Layer**: Aggregating data into business-level views like monthly revenue per zone.

## 🧹 Data Cleaning & Conflict Resolution
Special handling was applied to address common BigQuery/Parquet schema issues:
* **Column Removal (`ehail_fee`)**: 
    - The `ehail_fee` column was removed from the staging models.
    - **Reason**: The source Parquet files contained inconsistent data types (`DOUBLE` vs `INT64`) across different months, causing BigQuery external table read failures.
    - **Decision**: Since the column had a high null rate and was not critical for revenue analysis, it was dropped to ensure pipeline stability.
* **Type Matching**: Standardized `payment_type` across all models to resolve "Super type mismatch" errors during dbt tests.

## 🧪 Data Quality & Testing
Generic dbt tests are implemented to ensure data integrity:
- **Uniqueness**: Applied to `tripid` in core models.
- **Accepted Values**: Validating `payment_type` codes.
- **Non-null**: Enforced on critical timestamp and ID columns.
