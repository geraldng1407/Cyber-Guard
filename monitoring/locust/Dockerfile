FROM locustio/locust:latest

# Copy the custom script and the locustfile.py into the container
COPY run_locust.sh /usr/local/bin/run_locust.sh
# COPY locustfile.py /locustfile.py

# Make the script executable
USER root
RUN chmod +x /usr/local/bin/run_locust.sh

# Set the script as the entrypoint
ENTRYPOINT ["/usr/local/bin/run_locust.sh"]