from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import pika
import asyncio
import json
from clickhouse_driver import Client

# FastAPI App Setup
app = FastAPI()

# RabbitMQ Connection Setup
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'user_events'
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()

# ClickHouse Client Setup
CLICKHOUSE_HOST = 'localhost'
clickhouse_client = Client(CLICKHOUSE_HOST)

# Create table in ClickHouse if it doesn't exist
clickhouse_client.execute('''
CREATE TABLE IF NOT EXISTS user_events (
    event_id String,
    user_id String,
    event_type String,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY timestamp
''')

# WebSocket Connections storage
active_connections = []

# Helper Function: Insert event into ClickHouse
def insert_event_to_clickhouse(event_data):
    query = '''
    INSERT INTO user_events (event_id, user_id, event_type, timestamp) VALUES
    '''
    clickhouse_client.execute(query, [tuple(event_data.values())])

# RabbitMQ Consumer - Real-time event processing
def process_event(ch, method, properties, body):
    event_data = json.loads(body.decode())
    insert_event_to_clickhouse(event_data)
    # Broadcast data to all connected WebSocket clients
    for connection in active_connections:
        asyncio.create_task(connection.send_text(json.dumps(event_data)))

# Start consuming RabbitMQ queue
def start_rabbitmq_consumer():
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_event, auto_ack=True)
    channel.start_consuming()

# Run RabbitMQ Consumer in Background Thread
import threading
threading.Thread(target=start_rabbitmq_consumer, daemon=True).start()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Keep WebSocket connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.get("/analytics")
async def get_analytics():
    # Fetch real-time analytics from ClickHouse
    query = 'SELECT user_id, count(*) as event_count FROM user_events GROUP BY user_id ORDER BY event_count DESC LIMIT 10'
    result = clickhouse_client.execute(query)
    return JSONResponse(content=result)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

