from kafka import KafkaConsumer
from datetime import datetime
import time
import json
import threading

import mariadb
import uuid

consumer = KafkaConsumer('new_orders',
                         bootstrap_servers=["localhost:9092"],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         auto_commit_interval_ms=1000,
                         consumer_timeout_ms=1000
                         )

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'mysql',
    'database': 'mydb'
}

conn = mariadb.connect(**config)
cursor = conn.cursor()
sql = '''INSERT INTO delivery_status(delivery_id, order_json, status)
            VALUES(?, ?, ?)'''

def fetch_latest_orders(next_call_in):
    next_call_in += 30
    
    batch = consumer.poll(timeout_ms=100)
    if len(batch) > 0:
        for message in list(batch.values())[0]:
            value = message.value.decode()

            delivery_id = str(uuid.uuid4())
            status = 'CONFIRMED'
            # db insert 
            cursor.execute(sql, [delivery_id, value, status])
            conn.commit()

    threading.Timer(next_call_in - time.time(),
                    fetch_latest_orders,
                    [next_call_in]).start()

next_call_in = time.time()
fetch_latest_orders(next_call_in)
