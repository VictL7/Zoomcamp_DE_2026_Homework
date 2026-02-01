# 📘 Zoomcamp_DE_2026_Homework

This repository contains my homework for the **Data Engineering Zoomcamp 2026** by DataTalksClub.  


- **1.1 Docker Data Ingestion** – building a containerized data pipeline  
- **1.2 Terraform & GCP** – provisioning cloud infrastructure for data storage and processing
- **2.1 Kestra Workflow Orchestration** – parameterized ingestion pipelines, backfill, scheduling, and a simple RAG workflow  


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
├── 2_Kestra_work_orchestration/ # Kestra workflows (Week 2)
│ ├── 01_gcp_kv_taxi.yaml # Store GCP config in KV
│ ├── 02_gcp_setup_taxi.yaml # Create GCS bucket & BigQuery dataset
│ ├── 03_gcp_taxi_ingest.yaml # Parameterized ingestion of taxi CSVs
│ ├── 04_gcp_taxi_scheduled_backfill.yaml # Backfill & scheduled workflows
│ ├── 05_chat_with_rag.yaml # RAG workflow using Zoomcamp docs
│ ├── Docker_Compose.yaml # Local Kestra + Postgres + pgAdmin setup
│ └── README.md # Detailed instructions for Kestra flows
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
# ⚡ 2.1 Kestra Workflow Orchestration

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
# 📌 Notes

This repository is part of my learning journey through the Data Engineering Zoomcamp.  
Each module includes its own README with detailed instructions, code, and explanations.

