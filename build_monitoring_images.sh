#!/bin/bash

# Build Docker images
echo "Building Docker images..."
# Monitoring environment services 
docker build -t cyberguard_fastapi:latest ./monitoring/fastapi_endpoints
docker build -t database_fastapi:latest ./monitoring/database_fastapi
docker build -t mysql_image:latest ./monitoring/database
docker build -t login_fastapi:latest ./monitoring/login-app
docker build -t flask_app:latest ./monitoring/flask-app

# Run docker-compose up
echo "Starting containers in monitoring using docker-compose..."

docker plugin enable loki
docker-compose -f monitoring/docker-compose.yaml up -d