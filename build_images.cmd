@echo off

echo Building Docker images...

docker build -t anomaly_detector:latest .\anomaly_detection
docker build -t cyberguard_fastapi:latest .\fastapi_endpoints
docker build -t database_fastapi:latest .\database_fastapi
docker build -t mysql_image:latest .\database
docker build -t login_fastapi:latest .\login-app
docker build -t flask_app:latest .\flask-app
docker build -t metrics_service:latest .\backend/MetricsService
docker build -t alerts_db:latest .\backend\alertsDB
docker build -t notifications_service:latest .\backend\NotificationsService
docker build -t notifications_db:latest .\backend\NotificationsDB
echo Starting containers using docker-compose...

docker-compose up -d    
