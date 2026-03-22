# 7_Streaming (Flink + Redpanda + Postgres)

## Project Purpose

This project demonstrates a simple streaming data pipeline using:

- **Redpanda (Kafka API)** as the message broker
- **Apache Flink** for stream processing and window aggregations
- **PostgreSQL** as the sink storage

Main workflow:

1. `producer.py` publishes NYC Green Taxi trip events to topic `green-trips`.
2. Flink jobs consume the stream and compute aggregations.
3. Results are written to PostgreSQL tables.

---

## How to Start the Project

Run all commands from the `7_Streaming` folder.

### 1) Start infrastructure services

```bash
docker compose up -d
docker compose ps
```

### 2) Send data to the topic

```bash
source .venv/bin/activate
python src/producers/producer.py
```

### 3) Run the Flink job

`q6.py`

- Purpose: uses a **1-hour tumbling window** to compute total `tip_amount` per hour across all locations.

```bash
docker compose exec jobmanager ./bin/flink run \
	-py /opt/src/job/q6.py \
	--pyFiles /opt/src
```


`pass_through_job.py`

- Purpose: uses a **5-minute tumbling window** to count trips per `PULocationID`.

```bash
docker compose exec jobmanager ./bin/flink run \
	-py /opt/src/job/pass_through_job.py \
	--pyFiles /opt/src
```

`session_window.py`

- Purpose: uses a **5-minute session window** to count trips per `PULocationID` by active sessions.

```bash
docker compose exec jobmanager ./bin/flink run \
	-py /opt/src/job/session_window.py \
	--pyFiles /opt/src
```

---

## Project Structure

```text
7_Streaming/
├── docker-compose.yml
├── Dockerfile.flink
├── pyproject.toml
├── uv.lock
├── main.py
├── README.md
└── src/
		├── models.py
		├── producers/
		│   └── producer.py
		├── consumers/
		│   ├── consumer.py
		│   └── consumer_postgres.py
		└── job/
				├── pass_through_job.py
				├── session_window.py
				└── q6.py
```

Job file summary:

- `pass_through_job.py`: 5-minute tumbling window trip count by pickup location.
- `session_window.py`: 5-minute session window trip count by pickup location.
- `q6.py`: 1-hour tumbling window total `tip_amount` across all locations.
