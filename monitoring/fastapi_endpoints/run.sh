#!/bin/bash

# Start the app in the background
python /app/app.py &

# Start Locust
locust -f /locustfile.py --headless --users 10 --spawn-rate 1 -H http://localhost:8000