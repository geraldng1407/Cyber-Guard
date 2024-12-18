import logging
import os
from typing import Optional

import httpx
import uvicorn
import json
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from opentelemetry.propagate import inject
from utils import PrometheusMiddleware, metrics, setting_otlp
from faker import Faker
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager

# Environment variables
APP_NAME = os.environ.get("APP_NAME", "app")
EXPOSE_PORT = int(os.environ.get("EXPOSE_PORT", 8000))
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")
latitude = os.getenv('LATITUDE', 'Unknown')
longitude = os.getenv('LONGITUDE', 'Unknown')

app = FastAPI()

# Setting metrics middleware
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Log format with geographical coordinates and trace info
log_format = (
    f"%(asctime)s - [Lat: {latitude}, Lon: {longitude}] - %(levelname)s "
    "[%(name)s] [%(filename)s:%(lineno)d] "
    "[trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] "
    "- %(message)s"
)

class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1

# Basic logging configuration
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger(APP_NAME)
logger.addFilter(EndpointFilter())
setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)

fake = Faker()

# Generate fake users
fake_users_db = {
    # fake.user_name(): {
    #     "username": fake.user_name(),
    #     "password": fake.password(),
    #     "ip": fake.ipv4()
    # }
    # for _ in range(10)  # Generate 10 fake users
}

# Add a few known users to test
fake_users_db.update({
    "johndoe": {
        "username": "johndoe",
        "password": "secretpassword",
        "ip": "192.168.0.1"
    },
    # "peterlim": {
    #     "username": "peterlim",
    #     "password": "secretpassword",
    #     "ip": "192.168.0.5"
    # }
})

# Pydantic model for request body
class LoginRequest(BaseModel):
    username: str
    password: str

class PasswordResetRequest(BaseModel):
    username: str

@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    try:
        # Parse the request body as JSON
        body_json = json.loads(body)
        username = body_json.get("username")
    except (json.JSONDecodeError, TypeError):
        # Default to actual IP if request body parsing fails
        username = None

    client_ip = request.client.host
    if username and username in fake_users_db:
        client_ip = fake_users_db[username]["ip"]

    method = request.method
    url = request.url.path
    user_agent = request.headers.get("user-agent", "-")
    
    # logger.info(f"Request - Client IP: {client_ip}, Method: {method}, URL: {url}, User-Agent: {user_agent}")
    
    response = await call_next(request)
    
    log_data = {
        'clientip': client_ip,
        'method': method,
        'url': url,
        'status': response.status_code,
        'size': response.headers.get("content-length", 0),
        'user_agent': user_agent
    }
    
    logger.info(f"Response - {log_data}")
    return response

@app.get("/fake_users")
async def get_fake_users():
    return fake_users_db

@app.post("/login")
async def login(request: LoginRequest):
    username = request.username
    password = request.password
    
    # Check if user exists and password matches
    if username in fake_users_db and fake_users_db[username]["password"] == password:
        logger.info(f"Successful login for user: {username}")
        return {"message": f"Welcome {username}!"}
    else:
        logger.error(f"Failed login attempt for user: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.post("/forget_password")
async def forget_password(request: PasswordResetRequest):
    username = request.username
    if username in fake_users_db:
        # logger.info(f"Password reset for user: {username}")
        return {"message": "Password reset initiated"}
    else:
        # logger.error(f"Password reset failed for user: {username}")
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/start")
async def start():
    return {"message": "Access to the starting page granted"}

if __name__ == "__main__":
    # Update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = (
        f"%(asctime)s - [Lat: {latitude}, Lon: {longitude}] - %(levelname)s "
        "[%(name)s] [%(filename)s:%(lineno)d] "
        "[trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] "
        "- %(message)s"
    )
    
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, log_config=log_config)