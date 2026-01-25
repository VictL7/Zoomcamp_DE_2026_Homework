# 📘 Zoomcamp_DE_2026_Homework

This repository contains my homework for the **Data Engineering Zoomcamp 2026** by DataTalksClub.  


- **1.1 Docker Data Ingestion** – building a containerized data pipeline  
- **1.2 Terraform & GCP** – provisioning cloud infrastructure for data storage and processing  

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

# 📌 Notes

This repository is part of my learning journey through the Data Engineering Zoomcamp.  
Each module includes its own README with detailed instructions, code, and explanations.

