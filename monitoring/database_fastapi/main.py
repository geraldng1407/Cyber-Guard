import logging
import os
import random
import time
from typing import Optional

import uvicorn
from fastapi import FastAPI, Response
from opentelemetry.propagate import inject
from utils import PrometheusMiddleware, metrics, setting_otlp
import mysql.connector
from prometheus_fastapi_instrumentator import Instrumentator

APP_NAME = os.environ.get("APP_NAME", "database-app")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")
country = os.getenv('COUNTRY', 'Unknown')
code = os.getenv('CODE', 'Unknown')
container_name = os.environ.get("CONTAINER_NAME", "Unknown"),
instance = os.environ.get("INSTANCE", "Unknown"),

app = FastAPI()

log_format = (
    f"%(asctime)s - [Country: {country}, Code: {code}] - %(levelname)s "
    "[%(name)s] [%(filename)s:%(lineno)d] "
    "[trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] "
    "- %(message)s"
)

logging.basicConfig(format=log_format,level=logging.ERROR)

# Retrieve database connection details from environment variables
db_host = os.getenv('DB_HOST', 'mysql')
# db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('MYSQL_ROOT_PASSWORD', 'password')
db_name = os.getenv('MYSQL_DATABASE', 'db')

# Setting metrics middleware
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Setting OpenTelemetry exporter
setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)


class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


def get_db_connection():
    return mysql.connector.connect(
        host=db_host,
        # user=db_user,
        password=db_password,
        database=db_name
    )

@app.get("/test")
async def read_root():
    logging.error("Testing")
    return "Testing page for database app"

@app.get("/insert_user/{username}/{email}")
async def insert_user(username: str, email: str):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        connection.commit()
        cursor.close()
        connection.close()
        logging.error(f"Inserted user: {username} with email: {email}")
        return {"username": username, "email": email}
    except Exception as e:
        logging.error("Failed to insert user", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/select_user/{user_id}")
async def select_user(user_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user:
            return {"user": {"id": user[0], "username": user[1], "email": user[2], "created_at": user[3]}}
        else:
            return {"message": "User not found"}
    except Exception as e:
        logging.error("Failed to select user", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
if __name__ == "__main__":

    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = log_format #f"%(asctime)s - [Lat: {latitude}, Lon: {longitude}] - %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, log_config=log_config)
