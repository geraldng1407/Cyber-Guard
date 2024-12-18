import logging
import os
import random
import time
from typing import Optional

import httpx
import uvicorn
from fastapi import FastAPI, Response, Request
from opentelemetry.propagate import inject
from utils import PrometheusMiddleware, metrics, setting_otlp

APP_NAME = os.environ.get("APP_NAME", "login-app")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")
latitude = os.getenv('LATITUDE', 'Unknown')
longitude = os.getenv('LONGITUDE', 'Unknown')

app = FastAPI()

# Setting metrics middleware
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)

# Setting OpenTelemetry exporter
setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)

class AccessLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        logger.info(log_entry)

class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1

#Apache Style log format
formatter = logging.Formatter('%(clientip)s - - [%(asctime)s] "%(method)s %(url)s HTTP/1.1" %(status)s %(size)s "-" "%(user_agent)s"')
logging.basicConfig(level=logging.INFO)
# Filter out /endpoint
logger = logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
log_handler = AccessLogHandler()
log_handler.setFormatter(formatter) 

@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_ip = request.client.host
    method = request.method
    url = request.url.path
    user_agent = request.headers.get("user-agent", "-")
    
    response = await call_next(request)
    
    log_data = {
        'clientip': client_ip,
        'method': method,
        'url': url,
        'status': response.status_code,
        'size': response.headers.get("content-length", 0),
        'user_agent': user_agent
    }
    
    logger.info(log_data)
    return response

# Example endpoints
@app.get("/login")
async def login(response: Response):
    if random.choice([True, False]):
        response.status_code = 200
        return {"message": "Login successful"}
    else:
        response.status_code = 401
        return {"message": "Login failed"}

@app.get("/random_status")
async def random_status(response: Response):
    response.status_code = random.choice([200, 300, 400, 500])
    logger.info(f"Random status code: {response.status_code}")
    return {"status": response.status_code}


if __name__ == "__main__":

    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = f"%(asctime)s - [Lat: {latitude}, Lon: {longitude}] - %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, log_config=log_config)