import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import psycopg2
from kafka import KafkaConsumer
from models import ride_deserializer

server = 'localhost:9092'
topic_name = 'green-trips'        # same topic as producer

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='postgres',
    user='postgres',
    password='postgres'
)
conn.autocommit = True
cur = conn.cursor()

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',
    group_id='green-trips-to-postgres',
    value_deserializer=ride_deserializer
)

print(f"Listening to {topic_name} and writing to PostgreSQL...")

count = 0
for message in consumer:
    try:
        ride = message.value
        pickup_dt = datetime.strptime(ride.lpep_pickup_datetime, "%Y-%m-%d %H:%M:%S")
        dropoff_dt = datetime.strptime(ride.lpep_dropoff_datetime, "%Y-%m-%d %H:%M:%S")

        cur.execute(
            """INSERT INTO green_trips     
                (lpep_pickup_datetime, lpep_dropoff_datetime,
                 PULocationID, DOLocationID, passenger_count,
                 trip_distance, tip_amount, total_amount)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (pickup_dt, dropoff_dt,
             ride.PULocationID, ride.DOLocationID,
             ride.passenger_count, ride.trip_distance,
             ride.tip_amount, ride.total_amount)
        )
        count += 1
        if count % 100 == 0:
            print(f"Inserted {count} rows...")

    except Exception as e:
        print(f"Error inserting row: {e}")
        continue

consumer.close()
cur.close()
conn.close()