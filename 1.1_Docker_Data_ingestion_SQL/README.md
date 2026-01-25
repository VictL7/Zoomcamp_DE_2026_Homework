# NYC Green Taxi Data Ingestion Pipeline

This project is part of the **DataTalksClub Data Engineering Zoomcamp**.  
It implements a containerized data ingestion pipeline that loads NYC Green Taxi trip data into PostgreSQL for analysis.

---

## Project Overview

The pipeline performs the following steps:

1. Downloads NYC Green Taxi trip data (Parquet format)
2. Loads Taxi Zone lookup data (CSV format)
3. Applies explicit data type casting
4. Ingests the data into a PostgreSQL database
5. Enables SQL-based analytics via pgAdmin

All services are containerized using **Docker** and orchestrated with **Docker Compose**.

---

## Tech Stack

- **Python 3.13**
- **pandas / pyarrow** – data processing
- **PostgreSQL 18** – analytical database
- **pgAdmin 4** – database administration UI
- **Docker & Docker Compose**
- **uv** – Python dependency management

---

## Project Structure

```text
.
├── Data_ingest.py        # Main ingestion pipeline
├── Data_ingest.ipynb     # Exploratory / development notebook
├── Dockerfile            # Docker image for ingestion pipeline
├── docker-compose.yaml   # PostgreSQL + pgAdmin services
├── pyproject.toml        # Python dependencies
├── uv.lock               # Locked dependency versions
├── .gitignore
└── README.md
```

---

# Data Sources

### **NYC Green Taxi Trip Data (Parquet)**  
https://d37ci6vzurychx.cloudfront.net/trip-data/

### **Taxi Zone Lookup Table (CSV)**  
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

### **Why two datasets?**
- Trip data contains **trip-level fact data**  
- Zone lookup table provides **dimension data** (LocationID → Zone / Borough)

---

# How to Run

## 1. Start PostgreSQL and pgAdmin

```bash
docker-compose up -d
```

pgAdmin will be available at:  
**http://localhost:8085**

---

## 2. Build the ingestion image

```bash
docker build -t taxi_ingest:v001 .
```

---

## 3. Run the ingestion pipeline

```bash
docker run -it --rm \
  --network zoomcamp_de_2026_homework_pgnetwork \
  taxi_ingest:v001 \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=pgdatabase \
  --pg-port=5432 \
  --pg-db=ny_taxi
```

---

# pgAdmin Access

### URL  
http://localhost:8085

### Login  
- **Email:** admin@admin.com  
- **Password:** root  

### PostgreSQL connection settings  
| Setting | Value |
|--------|--------|
| Host | pgdatabase |
| Port | 5432 |
| Database | ny_taxi |
| User | root |
| Password | root |

---

# Notes

- Raw data files are **not committed** to the repository  
- PostgreSQL data is **persisted using Docker volumes**  
- The ingestion container is **stateless** and can be safely re-run  

---

# Homework SQL Answers

## Trips in November 2025 with `trip_distance` ≤ 1 mile

```sql
SELECT COUNT(*)
FROM public.green_taxi_data
WHERE lpep_pickup_datetime >= DATE '2025-11-01'
  AND lpep_pickup_datetime <  DATE '2025-12-01'
  AND trip_distance <= 1;
```

**Answer: 8007**

---

## Day with the longest trip distance (only trips < 100 miles)

```sql
SELECT
  trip_distance,
  lpep_pickup_datetime
FROM public.green_taxi_data
WHERE trip_distance <= 100
ORDER BY trip_distance DESC
LIMIT 1;
```

**Answer:**  
- **Distance:** 88.03 miles  
- **Pickup time:** `"2025-11-14 15:36:27"`

---

## Pickup zone with the largest `total_amount` on 2025‑11‑18

```sql
SELECT
    z."Zone",
    SUM(t.total_amount) AS total_amount
FROM public.green_taxi_data t
JOIN public.taxi_zone z
    ON t."PULocationID" = z."LocationID"
WHERE t.lpep_pickup_datetime::date = DATE '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_amount DESC
LIMIT 1;
```

**Answer:**  
**East Harlem North — 9281.92**

---

## For passengers picked up in **East Harlem North** in November 2025,  
### which dropoff zone had the **largest tip**?

```sql
SELECT
    dz."Zone" AS dropoff_zone,
    t.tip_amount
FROM public.green_taxi_data t
JOIN public.taxi_zone pz
    ON t."PULocationID" = pz."LocationID"
JOIN public.taxi_zone dz
    ON t."DOLocationID" = dz."LocationID"
WHERE
    pz."Zone" = 'East Harlem North'
    AND t.lpep_pickup_datetime >= '2025-11-01'
    AND t.lpep_pickup_datetime <  '2025-12-01'
ORDER BY t.tip_amount DESC
LIMIT 1;
```

**Answer:**  
| dropoff_zone   | tip_amount |
|----------------|------------|
| **Yorkville West** | **81.89** |

---

