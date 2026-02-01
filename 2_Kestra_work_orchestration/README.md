# 📦 Data Engineering Zoomcamp – Week 2 Homework (Kestra)

This repository contains my homework for **Data Engineering Zoomcamp – Week 2 (Workflow Orchestration)**.

The project demonstrates how to use **Kestra** to orchestrate data ingestion pipelines and a simple RAG (Retrieval-Augmented Generation) workflow.

### The workflows cover:
* **GCP setup** (GCS + BigQuery)
* **Parameterized** taxi data ingestion
* **Backfill and scheduling**
* **Minimal RAG example** using course documentation

---

## 🧱 Project Structure
All workflows are written in Kestra YAML and organized by purpose.

```text
.
├── Docker_Compose.yaml
├── 01_gcp_kv_taxi.yaml
├── 02_gcp_setup_taxi.yaml
├── 03_gcp_taxi_ingest.yaml
├── 04_gcp_taxi_scheduled_backfill.yaml
└── 05_chat_with_rag.yaml

```
## 🐳 Docker Setup

### `Docker_Compose.yaml`
This file sets up the local development environment using Docker Compose. It includes:

* **PostgreSQL** for taxi data
* **PostgreSQL** for Kestra metadata
* **Kestra server** (standalone mode)
* **pgAdmin** for database inspection

> This setup allows running Kestra locally and executing all workflows without external orchestration tools.

---

## 🔐 Workflow Descriptions

### 1️⃣ `01_gcp_kv_taxi.yaml` – GCP Configuration via KV Store
This workflow initializes global configuration values using Kestra’s KV store. It stores:
* GCP Project ID
* GCP Location
* GCS Bucket name
* BigQuery Dataset name
* (Separately) GCP service account credentials

**Purpose:** Centralize configuration and secrets so they are not hard-coded in ingestion workflows.

---

### 2️⃣ `02_gcp_setup_taxi.yaml` – GCP Resource Setup
This workflow creates required GCP resources:
* Google Cloud Storage bucket
* BigQuery dataset

**Key Feature:** The workflow is **idempotent** (if resources already exist, they are skipped).

**Purpose:** Ensure infrastructure is ready before running any ingestion jobs.

---

### 3️⃣ `03_gcp_taxi_ingest.yaml` – Parameterized Taxi Data Ingestion
This workflow ingests NYC Taxi CSV data into GCP. Key features:
* **Parameterized inputs** (taxi type, year, month)
* Downloads data from the public Zoomcamp dataset
* Uploads raw files to GCS
* Loads data into BigQuery tables

**Purpose:** Demonstrate a reusable ingestion pipeline that can handle different taxi types and dates.

---

### 4️⃣ `04_gcp_taxi_scheduled_backfill.yaml` – Backfill & Scheduling
This workflow extends the ingestion logic with:
* **Scheduled execution** (monthly)
* **Manual backfill support** for historical data
* Explicit input-driven execution (no dependency on trigger dates)

**Purpose:** Show how Kestra can be used both for historical data backfill and ongoing production-style scheduling.

---

### 5️⃣ `05_chat_with_rag.yaml` – Simple RAG Workflow
This workflow demonstrates a homework-level RAG (Retrieval-Augmented Generation) pipeline using Kestra. Steps:
* Ingest the official Data Engineering Zoomcamp README
* Generate embeddings using an LLM provider
* Answer a career-related question using retrieved context

**Note:** The workflow is intentionally minimal and avoids hallucination by using only provided documentation and explicitly instructing the model to rely on retrieved context.

**Purpose:** Illustrate how Kestra can orchestrate AI-related workflows in addition to data pipelines.

---

## 🎯 Key Learning Outcomes
Through this homework, I practiced:
* **Workflow orchestration** with Kestra
* **Parameterized** and reusable pipelines
* **Backfill vs scheduled** execution
* **Secure handling** of configuration and secrets
* Basic **RAG concepts** integrated into a workflow system

---

## 📝 Notes
* **Security:** Secrets (API keys, service account credentials) are stored in Kestra KV and are **not** committed to the repository.
* **Clarity:** All workflows are designed for educational purposes rather than production hardening.

---

## ✅ Status
All workflows have been tested locally using Docker Compose and executed successfully in Kestra.
