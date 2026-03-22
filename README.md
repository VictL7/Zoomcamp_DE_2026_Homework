# 📘 Zoomcamp_DE_2026_Homework

This repository contains my homework for the **Data Engineering Zoomcamp 2026** by DataTalksClub.  


- **1.1 Docker Data Ingestion** – building a containerized data pipeline  
- **1.2 Terraform & GCP** – provisioning cloud infrastructure for data storage and processing
- **2. Kestra Workflow Orchestration** – parameterized ingestion pipelines, backfill, scheduling, and a simple RAG workflow  
- **3. BigQuery Data Warehousing** - mastering columnar storage, Partitioning, Clustering, and cost-effective data strategies.
- **4. Analytics Engineering (dbt + BigQuery)** – medallion modeling, tests, and revenue-ready marts
- **5. Data Platforms (Bruin)** – ingestion → staging → reporting with lineage and validation
- **6. Batch Processing (PySpark SQL)** – Spark DataFrame/SQL analysis over NYC Yellow Taxi data
- **7. Stream Processing (Flink)** – Real-time data pipelines with Flink, Redpanda, and window aggregations
- **Workshop: dlt APIs to Warehouses** – paginated API ingestion with dlt into DuckDB


---

# 📂 Project Structure

```
.
├── 1.1_Docker_Data_ingestion_SQL/      # Docker + Data Ingestion pipeline
│   ├── ingestion/
│   │   ├── Data_ingest.py
│   │   ├── Data_ingest.ipynb
│   │   ├── Dockerfile
│   │   ├── docker-compose.yaml
│   │   ├── pyproject.toml
│   │   └── DOCKER_README.md
│   └── README.md
│
├── 1.2_Terraform_GCP/                  # Terraform + GCP environment
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
│
├── 2_Kestra_work_orchestration/        # Kestra workflows (Week 2)
│ ├── 01_gcp_kv_taxi.yaml               # Store GCP config in KV
│ ├── 02_gcp_setup_taxi.yaml            # Create GCS bucket & BigQuery dataset
│ ├── 03_gcp_taxi_ingest.yaml           # Parameterized ingestion of taxi CSVs
│ ├── 04_gcp_taxi_scheduled_backfill.yaml # Backfill & scheduled workflows
│ ├── 05_chat_with_rag.yaml             # RAG workflow using Zoomcamp docs
│ ├── Docker_Compose.yaml               # Local Kestra + Postgres + pgAdmin setup
│ └── README.md                         # Detailed instructions for Kestra flows
│
├── 3_data_warehouse_Bigquery/          # BigQuery Warehouse (Week 3)
│   ├── Bigquery_hw3.sql                # SQL queries for optimization & analysis
│   ├── load_yellow_taxi_data.py        # Python script to load Parquet to GCS
│   ├── requirements.txt                # Python dependencies
│   └── README.md                       # Week 3 specific documentation
│
├── 4_Analytics_Engineering_dbt/        # dbt models and analytics engineering (Week 4)
│   ├── dbt_cloud_nytaxi/               # Main NYC taxi dbt project README + models/macros
│   ├── nytaxi/                         # Local dbt scaffold/project files
│   └── load_taxi_data_GCP.py
│
├── 5_data_platforms/
│   └── my-taxi-pipeline/               # Bruin pipeline (ingestion/staging/reports)
│       ├── pipeline/pipeline.yml
│       └── README.md
│
├── 6_Batch/                            # PySpark SQL batching practice
│   ├── pyspark_SQL.ipynb
│   └── README.md
│
├── 7_Streaming/                        # Flink stream processing (Week 7)
│   ├── src/
│   │   ├── models.py
│   │   ├── producers/producer.py       # Kafka producer for taxi events
│   │   ├── consumers/                  # Consumer implementations
│   │   └── job/                        # Flink jobs
│   │       ├── q6.py                   # 1-hour tumbling window for hourly tips
│   │       ├── pass_through_job.py     # 5-minute tumbling window by location
│   │       └── session_window.py       # 5-minute session window by location
│   ├── docker-compose.yml
│   ├── Dockerfile.flink
│   ├── pyproject.toml
│   └── README.md
│
├── workshop_dlt_APIs_to_Warehouses/    # dlt + uv + MCP workshop
│   ├── SETUP_GUIDE.md
│   └── taxi_pipeline/
│       ├── taxi_pipeline.py
│       └── README.md
│
└── README.md                           # This file
```

---

# 🚀 1.1 Docker Data Ingestion

This module implements an end-to-end pipeline for **NYC Green Taxi data**:

- Downloads NYC Green Taxi trip data (Parquet) and Taxi Zone Lookup (CSV)
- Processes data using **Python (pandas / pyarrow)**
- Ingests data into **PostgreSQL** running inside Docker
- Provides SQL access through **pgAdmin**
- Fully containerized using **Docker & Docker Compose**

### 🔑 Key Learnings

- Container networking and orchestration with Docker Compose  
- Debugging PostgreSQL connection issues  
- Organizing project files and Docker volumes for persistent data  
- Hands-on experience writing SQL queries for analytics  

---

# ☁️ 1.2 Terraform & GCP

This module sets up cloud infrastructure for data pipelines using **Terraform**:

- Provisions resources on **Google Cloud Platform (GCP)**
- Creates a **GCS bucket** for raw data storage
- Creates a **BigQuery dataset** for analytical queries
- Demonstrates **Infrastructure as Code (IaC)** principles

### 🔑 Key Learnings

- Defining cloud resources using Terraform configuration files  
- Deploying, modifying, and destroying infrastructure programmatically  
- Understanding **BigQuery** as a managed data warehouse  
- Integrating local, VM, and cloud environments for reproducible pipelines  

---
# ⚡ 2. Kestra Workflow Orchestration

This module demonstrates **workflow orchestration using Kestra**, including:

- Parameterized ingestion pipelines for **NYC Taxi data**
- Backfill support for historical CSV data
- Scheduled workflows (monthly ingestion)
- Integration with **GCP** (GCS & BigQuery)
- A minimal **RAG (Retrieval-Augmented Generation) workflow** using course documentation

  
### 🔑 Key Learnings

- Using **Kestra** for orchestration and scheduling
- Parameterizing workflows for **reusable pipelines**
- Backfill vs scheduled execution
- Secure management of **configuration and secrets**
- Integrating **data ingestion** with cloud storage (GCS) and analytics (BigQuery)
- Introduction to **RAG workflows** in a data engineering context

---
## 📊 3. BigQuery Data Warehousing

This module focuses on building a high-performance **Data Warehouse** using **Google BigQuery** with **2024 NYC Yellow Taxi** data.

- Storage Architectures: Comparison between **External Tables** (GCS-backed) and **Native Tables** (BigQuery-backed)
- **Columnar Storage**: Understanding how BigQuery optimizes scan volume by reading only the required columns
- Query Optimization: Implementing **Partitioning** and **Clustering** to minimize costs and maximize query performance


## 🔑 Key Learnings

### Columnar Storage Efficiency
- Leveraged BigQuery’s ability to prune columns  
- Avoided `SELECT *` to significantly reduce query costs

### Partitioning Strategy
- Partitioned tables by `tpep_dropoff_datetime` (Day)  
- Enabled BigQuery to skip scanning irrelevant date ranges

### Clustering Strategy
- Clustered data by `VendorID` within partitions  
- Improved performance for sorting and filtering operations

### Best Practices
- Avoid clustering on small tables (< 1GB), where the overhead outweighs performance benefits  
- Native tables provide significantly better performance than external tables due to optimized metadata handling
- Table Size Threshold: Learned that clustering is generally recommended only for **tables > 1 GB** to ensure the performance gain outweighs the metadata management overhead
- **Metadata Optimization**: Observed that Native Tables leverage built-in metadata (like row counts) much faster than External Tables

---

## 🧱 4. Analytics Engineering with dbt (BigQuery)

This module focuses on transforming raw NYC taxi datasets into analytics-ready models using **dbt** and **BigQuery**.

- Main project docs are in [4_Analytics_Engineering_dbt/dbt_cloud_nytaxi/README.md](4_Analytics_Engineering_dbt/dbt_cloud_nytaxi/README.md)
- Architecture follows **Staging → Core → Marts**
- Includes schema harmonization and conflict handling (for example, dropping unstable `ehail_fee` to avoid type conflicts)
- Applies dbt tests for:
	- uniqueness (`tripid`)
	- accepted values (`payment_type`)
	- non-null critical keys/timestamps

### 🔑 Key Learnings
- Building maintainable dbt models with modular layers
- Handling external table schema inconsistencies safely
- Enforcing data quality with reusable generic tests

---

## 🏗️ 5. Data Platforms (Bruin)

This module implements a compact ELT workflow using **Bruin** in [5_data_platforms/my-taxi-pipeline](5_data_platforms/my-taxi-pipeline).

- Ingestion assets pull/normalize Yellow & Green trip data
- Staging SQL performs cleaning and deduplication
- Report assets generate daily trip aggregates
- Includes pipeline definition and lineage artifacts

### 🔑 Key Learnings
- End-to-end asset-based pipeline design
- Fast validation, targeted reruns, and lineage-driven debugging
- Correct aggregation at each layer (staging `COUNT(*)` vs report `SUM(trip_count)`)

---

## ⚙️ 6. Batch Processing with PySpark SQL

The batch module is maintained in [6_Batch](6_Batch) (course week label: 6_Batching).

- Notebook-based Spark workflow in [6_Batch/pyspark_SQL.ipynb](6_Batch/pyspark_SQL.ipynb)
- Reads NYC Yellow Taxi Parquet data and runs Spark SQL analysis
- Joins with zone lookup data and builds reporting queries
- Uses local partitioned parquet output for practice

### 🔑 Key Learnings
- Creating and managing `SparkSession`
- Schema inspection and SQL over temp views
- Joining fact and lookup datasets with Spark DataFrames

---

## 🚦 7. Stream Processing with Flink

Stream processing module is maintained in [7_Streaming](7_Streaming).

- Uses **Apache Flink** for stream processing and window aggregations
- **Redpanda** (Kafka API) as the message broker
- **PostgreSQL** for sink storage
- Processes NYC Green Taxi trip events with tumbling and session windows
- Includes Q6 task: 1-hour tumbling window to compute hourly tip totals

### 🔑 Key Learnings
- Building real-time data pipelines with Flink
- Window functions: tumbling, sliding, and session windows
- Kafka/Redpanda topic management and stream consumption
- Docker Compose orchestration for multi-service streaming applications
- Aggregation patterns for streaming analytics

---

## 🧪 Workshop: dlt APIs to Warehouses

Workshop materials are in [workshop_dlt_APIs_to_Warehouses](workshop_dlt_APIs_to_Warehouses), with executable pipeline code in [workshop_dlt_APIs_to_Warehouses/taxi_pipeline](workshop_dlt_APIs_to_Warehouses/taxi_pipeline).

- Uses **dlt** with a custom paginated resource (`page=1,2,...`) against the Zoomcamp API
- Loads data into **DuckDB** dataset `nyc_taxi_data`
- Managed with **uv** dependencies
- Setup and integration details documented in [workshop_dlt_APIs_to_Warehouses/SETUP_GUIDE.md](workshop_dlt_APIs_to_Warehouses/SETUP_GUIDE.md)

### 🔑 Key Learnings
- Building robust API pagination loops
- Running reproducible local loads with dlt + DuckDB
- Using MCP tooling patterns for documentation and pipeline introspection


---

# 📌 Notes

This repository is part of my learning journey through the Data Engineering Zoomcamp.  
Each module includes its own README with detailed instructions, code, and explanations.

