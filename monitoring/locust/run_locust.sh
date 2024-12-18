#!/bin/bash

# Define an array of ports
# Generate ports from 8001 to 8053
# ports_8001_8053=($(seq 8001 8053))

# # Generate ports from 9001 to 9054
# ports_9001_9054=($(seq 9001 9054))

# # Combine both arrays
# ports=("${ports_8001_8053[@]}" "${ports_9001_9054[@]}")
ports=(9037 9024 8017 9012 8038 8050 8035 8031 8002 9013 9014 8029 8019 8024 8058 8027 9001 9011 8008 8044 8047 8049 8020 8030 8053 9002 8001 8026 8032 8042 8006 8011 8045 9008 9006 8012 8009 8014 9009 9017 8037 8013 8048)

# Define the number of users and spawn rate
users=10
spawn_rate=1

# Define the locust file
locustfile="./monitoring/locust/locustfile.py"
# locustfile_db="locustfile_database.py"

# Define the runtime duration in seconds
runtime=120  # Run Locust for 120 seconds
pids=()

stop_locust() {
  echo "Stopping all Locust processes..."
  for pid in "${pids[@]}"; do
    kill -SIGTERM $pid  # Send SIGTERM to stop the process gracefully
  done
  exit 0
}

trap stop_locust SIGINT SIGTERM

# Start Locust instances
for port in "${ports[@]}"; do
  echo "Starting Locust on port $port..."
  locust -f $locustfile --headless --users $users --spawn-rate $spawn_rate -H http://localhost:$port &
  pids+=($!)  # Save the process ID of the locust command
done

# for port in "${database_ports[@]}"; do
#   echo "Starting Locust for database app on port $port..."
#   locust -f $locustfile_db --headless --users $users --spawn-rate $spawn_rate -H http://localhost:$port &
#   pids+=($!)  # Save the process ID of the locust command
# done

# Wait for the specified duration
sleep $runtime

# Stop all Locust processes
echo "Stopping Locust processes..."
for pid in "${pids[@]}"; do
  kill $pid
done

# echo "All Locust processes have been stopped."
