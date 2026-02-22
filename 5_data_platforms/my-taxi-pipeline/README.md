# my-taxi-pipeline

A small Bruin-based data pipeline that ingests NYC taxi trip Parquet files (Yellow & Green),
normalizes them in a staging layer, and produces a daily trips report stored in DuckDB.

This repo is a learning / homework project (Zoomcamp) and includes assets for ingestion, staging and reporting.

Contents
- `pipeline/pipeline.yml` — Bruin pipeline definition and variables
- `pipeline/assets/ingestion/trips.py` — Python ingestion asset (downloads Parquet, standardizes columns)
- `pipeline/assets/ingestion/payment_lookup.asset.yml` & `payment_lookup.csv` — seed lookup for payment types
- `pipeline/assets/staging/trips.sql` — staging SQL (cleaning / dedup)
- `pipeline/assets/reports/trips_report.sql` — report SQL (daily aggregates)
- `pipeline/assets/lineage/trips_report_lineage.dot` — simple DOT file showing asset lineage

# Overview - End-to-End Data Platform

This hands-on tutorial guides you through building a **complete NYC Taxi data pipeline** from scratch using Bruin - a unified CLI tool for data ingestion, transformation, orchestration, and governance.

## Learning Goals

You'll learn to build a production-ready ELT pipeline that:
- **Ingests** real NYC taxi trip data from public APIs using Python
- **Transforms** and cleans raw data with SQL, applying incremental strategies and deduplication
- **Reports** aggregated analytics with built-in quality checks
- **Deploys** to cloud infrastructure (BigQuery)

This is a learn-by-doing experience with AI assistance available through Bruin MCP. Follow the comprehensive step-by-step tutorial section below.


## Pipeline Skeleton

The suggested structure separates ingestion, staging, and reporting, but you may structure your pipeline however you like.

The required parts of a Bruin project are:
- `.bruin.yml` in the root directory
- `pipeline.yml` in the `pipeline/` directory (or in the root directory if you keep everything flat)
- `assets/` folder next to `pipeline.yml` containing your Python, SQL, and YAML asset files

```text
zoomcamp/
├── .bruin.yml                              # Environments + connections (local DuckDB, BigQuery, etc.)
├── README.md                               # Learning goals, workflow, best practices
└── pipeline/
    ├── pipeline.yml                        # Pipeline name, schedule, variables
    └── assets/
        ├── ingestion/
        │   ├── trips.py                    # Python ingestion
        │   ├── requirements.txt            # Python dependencies for ingestion
        │   ├── payment_lookup.asset.yml    # Seed asset definition
        │   └── payment_lookup.csv          # Seed data
        ├── staging/
        │   └── trips.sql                   # Clean and transform
        └── reports/
            └── trips_report.sql            # Aggregation for analytics
```

## 💡 Core Concept: Avoiding the Aggregation Pitfall

A critical part of this project is understanding **Data Grain** (granularity). As data moves from the **Staging** layer to the **Report** layer, the way you calculate metrics must change.

### 1. Data Layers & Granularity

| Layer | What does one row represent? (Grain) | How to count total trips? |
| :--- | :--- | :--- |
| **Staging** | **A single trip** | `COUNT(*)` |
| **Reports** | **A daily summary** (Aggregated) | `SUM(trip_count)` |

### 2. Common Mistake: COUNT vs. SUM

When querying the final `reports.trips_report` table to find the total trips for January:

❌ **Incorrect Approach:**
```sql
SELECT taxi_type, COUNT(taxi_type) 
FROM reports.trips_report 
WHERE MONTH(trip_date) = 1
GROUP BY 1;
```

Result: You get the number of records/rows in the report table (e.g., ~150 rows).

Why it's wrong: This tells you how many "daily groups" exist, not how many people actually took a taxi.


✅ **Correct Approach:**

```sql
SELECT taxi_type, SUM(trip_count)
FROM reports.trips_report
WHERE MONTH(trip_date) = 1
GROUP BY 1;
```

Result: You get the actual total volume (e.g., ~1.36 million trips).

Why it's right: Since the report table is already pre-aggregated, you must sum up the previously counted totals.


#### Essential CLI Commands

The most common commands you'll use during development:

| Command | Purpose |
|---------|---------|
| `bruin validate <path>` | Check syntax and dependencies without running (fast!) |
| `bruin run <path>` | Execute pipeline or individual asset |
| `bruin run --downstream` | Run asset and all downstream dependencies |
| `bruin run --full-refresh` | Truncate and rebuild tables from scratch |
| `bruin lineage <path>` | View asset dependencies (upstream/downstream) |
| `bruin query --connection <conn> --query "..."` | Execute ad-hoc SQL queries |
| `bruin connections list` | List configured connections |
| `bruin connections ping <name>` | Test connection connectivity |

# Example setup
> bruin run ./pipeline/pipeline.yml --start-date 2021-01-01 --end-date 2021-03-01

export BRUIN_START_DATE="2024-01-01"
export BRUIN_END_DATE="2024-02-01"
export BRUIN_VARS='{"taxi_types": ["yellow", "green"]}'