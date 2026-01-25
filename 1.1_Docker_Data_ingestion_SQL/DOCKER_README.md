# NYC Taxi Data Ingestion - Docker Setup

This directory contains scripts to ingest NYC taxi zone and green taxi trip data into a PostgreSQL database using Docker.

## Files

- **`ingest_data.py`** - Main data ingestion script with Click CLI
- **`Dockerfile`** - Docker image configuration
- **`docker-compose.yml`** - Docker Compose configuration for PostgreSQL + data ingestion

## Quick Start

### Option 1: Run with Docker Compose (Recommended)

```bash
# Build and run all services (PostgreSQL + data ingestion)
docker-compose up --build

# Run with custom target table name and skip zones if table exists
docker-compose up --build
```

### Option 2: Run Containers Separately

```bash
# Start PostgreSQL only
docker-compose up postgres -d

# Run data ingestion
docker-compose run ingest \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=postgres \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=_green_taxi_data
```

### Option 3: Manual Docker Commands

```bash
# Build the image
docker build -t ny-taxi-ingest .

# Start PostgreSQL container
docker run -d \
  --name ny_taxi_db \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=ny_taxi \
  -p 5432:5432 \
  postgres:16-alpine

# Wait for PostgreSQL to be ready, then run ingestion
docker run --rm \
  --link ny_taxi_db \
  ny-taxi-ingest \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=ny_taxi_db \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=_green_taxi_data
```

## Command Line Options

```bash
python ingest_data.py --help
```

Options:
- `--pg-user` - PostgreSQL username (default: root)
- `--pg-pass` - PostgreSQL password (default: root)
- `--pg-host` - PostgreSQL host (default: localhost)
- `--pg-port` - PostgreSQL port (default: 5432)
- `--pg-db` - PostgreSQL database name (default: ny_taxi)
- `--zone-table` - Table name for taxi zones (default: taxi_zone)
- `--target-table` - Target table name for trip data (default: green_taxi_data)
- `--skip-zones` - Skip taxi zone ingestion if table already exists (flag)

## Examples

### Ingest with custom table names
```bash
docker-compose run ingest \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=postgres \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=_green_taxi_data \
  --zone-table=taxi_zones
```

### Skip zone ingestion and use existing table
```bash
docker-compose run ingest \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=postgres \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=_green_taxi_data \
  --skip-zones
```

## Data Flow

1. **Taxi Zones**: Downloads CSV from GitHub, converts data types, creates `taxi_zone` table
2. **Trip Data**: Downloads Parquet file, converts data types, chunks data with Dask, inserts into `_green_taxi_data` table

## Database Connection

From Docker container:
```bash
# Connect to PostgreSQL from another container
docker exec -it ny_taxi_db psql -U root -d ny_taxi

# Or from host (if port 5432 is exposed)
psql -h localhost -U root -d ny_taxi
```

## Troubleshooting

### PostgreSQL won't start
Check logs:
```bash
docker-compose logs postgres
```

### Connection refused
Ensure PostgreSQL container is running and healthy:
```bash
docker-compose ps
docker-compose logs postgres
```

### Data ingestion fails
Check the logs:
```bash
docker-compose logs ingest
```

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (deletes database data)
docker-compose down -v

# Remove images
docker rmi ny-taxi-ingest postgres:16-alpine
```
