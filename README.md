# CyberGuard SMU 

Set-up guide

To set up mock monitoring environment:  
For macOS:
```
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
chmod +x build_monitoring_images.sh
./build_monitoring_images.sh
```

To set up backend:  
For macOS:
```
chmod +x build_images.sh
./build_images.sh
```
Note: Upon starting the backend, config.json is created to store API key locally to access Grafana. Should monitoring environment be rebuilt and restarted, delete the config.json file to allow regeneration of API key for new instance of Grafana.

To set up frontend:
```
docker-compose -f frontend/docker-compose.yaml up -d
```

To simulate traffic to containers:  
For macOS:
```
chmod +x monitoring/locust/run_locust.sh
./monitoring/locust/run_locust.sh
```

To access frontend: [http://localhost:3001/](http://localhost:3001/)
Recommended to view at 50% zoom 