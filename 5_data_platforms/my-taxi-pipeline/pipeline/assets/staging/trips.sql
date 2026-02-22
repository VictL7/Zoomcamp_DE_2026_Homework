/* @bruin

# Docs:
# - Materialization: https://getbruin.com/docs/bruin/assets/materialization
# - Quality checks (built-ins): https://getbruin.com/docs/bruin/quality/available_checks
# - Custom checks: https://getbruin.com/docs/bruin/quality/custom

# TODO: Set the asset name (recommended: staging.trips).
name: staging.trips
# TODO: Set platform type.
# Docs: https://getbruin.com/docs/bruin/assets/sql
# suggested type: duckdb.sql
type: duckdb.sql
# TODO: Declare dependencies so `bruin run ... --downstream` and lineage work.
# Examples:
# depends:
#   - ingestion.trips
#   - ingestion.payment_lookup
depends:
  - ingestion.trips
  - ingestion.payment_lookup

# TODO: Choose time-based incremental processing if the dataset is naturally time-windowed.
# - This module expects you to use `time_interval` to reprocess only the requested window.
materialization:
  # What is materialization?
  # Materialization tells Bruin how to turn your SELECT query into a persisted dataset.
  # Docs: https://getbruin.com/docs/bruin/assets/materialization
  #
  # Materialization "type":
  # - table: persisted table
  # - view: persisted view (if the platform supports it)
  type: table
  # TODO: set a materialization strategy.
  # Docs: https://getbruin.com/docs/bruin/assets/materialization
  # suggested strategy: time_interval
  #
  # Incremental strategies (what does "incremental" mean?):
  # Incremental means you update only part of the destination instead of rebuilding everything every run.
  # In Bruin, this is controlled by `strategy` plus keys like `incremental_key` and `time_granularity`.
  #
  # Common strategies you can choose from (see docs for full list):
  # - create+replace (full rebuild)
  # - truncate+insert (full refresh without drop/create)
  # - append (insert new rows only)
  # - delete+insert (refresh partitions based on incremental_key values)
  # - merge (upsert based on primary key)
  # - time_interval (refresh rows within a time window)
  strategy: create+replace
# TODO: Define output columns, mark primary keys, and add a few checks.
columns:
  - name: pickup_datetime
    type: timestamp
    description: The timestamp when the trip started.
    primary_key: true
    nullable: false
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
    description: The timestamp when the trip ended.
    nullable: false
  - name: trip_distance
    type: double
    description: The distance of the trip in miles.
  - name: fare_amount
    type: double
    description: The fare amount for the trip.
    checks:
      - name: non_negative
  - name: payment_type
    type: integer
    description: The payment type code (1-4).
  - name: taxi_type
    type: string
    description: The type of taxi (yellow or green).

# TODO: Add one custom check that validates a staging invariant (uniqueness, ranges, etc.)
# Docs: https://getbruin.com/docs/bruin/quality/custom
custom_checks:
  - name: row_count_greater_than_zero
    description: Ensure that the staging table has at least one row.
    query: |
      -- TODO: return a single scalar (COUNT(*), etc.) that should match `value`
      SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END 
      FROM staging.trips
    value: 1

@bruin */

-- TODO: Write the staging SELECT query.
--
-- Purpose of staging:
-- - Clean and normalize schema from ingestion
-- - Deduplicate records (important if ingestion uses append strategy)
-- - Enrich with lookup tables (JOINs)
-- - Filter invalid rows (null PKs, negative values, etc.)
--
-- Why filter by {{ start_datetime }} / {{ end_datetime }}?
-- When using `time_interval` strategy, Bruin:
--   1. DELETES rows where `incremental_key` falls within the run's time window
--   2. INSERTS the result of your query
-- Therefore, your query MUST filter to the same time window so only that subset is inserted.
-- If you don't filter, you'll insert ALL data but only delete the window's data = duplicates.

WITH ranked AS (
  SELECT
    t.pickup_datetime,
    t.dropoff_datetime,
    t.trip_distance,
    t.fare_amount,
    t.payment_type,
    t.taxi_type,
    ROW_NUMBER() OVER (
      PARTITION BY t.pickup_datetime, t.dropoff_datetime, t.trip_distance, t.fare_amount
      ORDER BY t.pickup_datetime
    ) AS rn
  FROM ingestion.trips t
  WHERE t.pickup_datetime >= '{{ start_datetime }}'
    AND t.pickup_datetime < '{{ end_datetime }}'
    AND t.fare_amount >= 0  -- Filter out negative fares ---test results: column 'fare_amount' has 12942 negative values
)
SELECT
  pickup_datetime,
  dropoff_datetime,
  trip_distance,
  fare_amount,
  payment_type,
  taxi_type
FROM ranked
WHERE rn = 1
