# 6_Batch

This folder contains the batching homework practice with **PySpark SQL**.

## Folder contents

- `pyspark_SQL.ipynb` — main notebook for Spark DataFrame + Spark SQL exercises
- `main.py` — minimal Python entrypoint
- `pyproject.toml` / `uv.lock` — Python environment and dependencies (managed by `uv`)
- `taxi_zone_lookup.csv` — zone lookup dimension file
- `yellow_tripdata_2025-11.parquet/` — partitioned Parquet output generated in notebook

## Prerequisites

- Python `>=3.13`
- Java 17 (recommended for Spark compatibility)

## Setup

### 1) Install Java 17 (Homebrew)

```bash
brew install openjdk@17
```

Add to your shell profile (`~/.bashrc` or `~/.zshrc`):

```bash
export JAVA_HOME="$(brew --prefix openjdk@17)"
export PATH="$JAVA_HOME/bin:$PATH"
```

Verify:

```bash
java --version
```

### 2) Install Python dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or with `pip`:

```bash
pip install pyspark
```

## Run

### Notebook workflow

Open `pyspark_SQL.ipynb`, select the project kernel (`.venv`), then run cells in order:

1. create `SparkSession`
2. load `yellow_tripdata_2025-11.parquet`
3. run SQL queries on temporary tables
4. join with `taxi_zone_lookup.csv`

### Script workflow

```bash
uv run python main.py
```

## Notes

- Spark UI may bind to `4041`/`4042` if `4040` is already in use.
- If Java-related errors appear, confirm `JAVA_HOME` points to Java 17.
