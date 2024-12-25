# Real-Time User Analytics System

This is a **Real-Time User Analytics System** built using **FastAPI**, **RabbitMQ**, **ClickHouse**, and **WebSockets**. It is designed to handle millions of user events per hour, process them in real-time, and send live updates to clients connected via WebSockets.

## Features
- **Real-Time Event Processing**: Uses **RabbitMQ** for efficient event queuing and processing.
- **Data Storage**: Stores user event data in **ClickHouse** for high-performance querying.
- **Real-Time WebSocket Updates**: Sends real-time data updates to connected clients using **WebSockets**.
- **User Analytics**: Aggregates and provides real-time user engagement analytics.
- **Health Check API**: Exposes a simple health check endpoint to ensure the system is operational.

## Installation

To run the Real-Time User Analytics System, make sure you have **Python 3.7+** and the following services installed:
- **RabbitMQ**: To queue user events.
- **ClickHouse**: For storing and querying event data.

Install the required Python dependencies:

```bash
pip install fastapi[all] clickhouse-driver pika websockets uvicorn
```

## Running the Server

Start the server using **Uvicorn**:

```bash
uvicorn main:app --reload
```

This will run the server locally at `http://127.0.0.1:8000`.

## API Usage

1. **Real-Time WebSocket Data**
   - Open a WebSocket connection to receive real-time data updates:
     ```bash
     ws://127.0.0.1:8000/ws
     ```

2. **Get User Analytics**
   - Send a `GET` request to `/analytics` to get real-time user engagement data:
     ```bash
     curl 'http://127.0.0.1:8000/analytics'
     ```

3. **Health Check**
   - Check if the server is healthy by sending a `GET` request to `/health`:
     ```bash
     curl 'http://127.0.0.1:8000/health'
     ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Feel free to open issues or pull requests for any improvements or features you'd like to add!