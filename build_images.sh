#!/bin/bash

# Build Docker images
echo "Building Docker images..."
# Backend services 
docker build -t anomaly_detector:latest ./anomaly_detection
docker build -t metrics_service:latest ./backend/MetricsService
docker build -t metrics_db:latest ./backend/metricsDB
docker build -t notifications_service:latest ./backend/NotificationsService
docker build -t notifications_db:latest ./backend/NotificationsDB

# Run docker-compose up
echo "Starting containers using docker-compose..."

docker plugin enable loki
docker-compose up -d