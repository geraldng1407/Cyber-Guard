# import csv
# import json

# def clean_bom(dictionary):
#     """ Remove BOM from dictionary keys if present. """
#     new_dict = {}
#     for k, v in dictionary.items():
#         new_key = k.replace('\ufeff', '')  # Remove BOM
#         new_dict[new_key] = v
#     return new_dict

# # Open the CSV file for reading
# with open('./anomaly_detection/ExploreV4.csv', mode='r', encoding='utf-8-sig') as file:
#     # Use csv.DictReader to read the CSV file into a dictionary
#     reader = csv.DictReader(file)
    
#     # Convert the CSV data into a list of dictionaries with cleaned keys
#     data_list = [clean_bom(row) for row in reader]

# # Extract the first 30 entries
# first_30_entries = data_list[:30]

# # Convert the list of the first 30 dictionaries to JSON format
# json_data = json.dumps(first_30_entries, indent=4)

# # Save the JSON data to a file
# json_filename = './anomaly_detection/first_30_entries.json'
# with open(json_filename, 'w', encoding='utf-8') as json_file:
#     json_file.write(json_data)

# print(f"First 30 entries have been saved to '{json_filename}'")
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
from utils import preprocess_dataframe, create_dummy
import keras
import tensorflow
app = FastAPI()

class Log(BaseModel):
    Time: str
    Line: str
    tsNs: str
    id: str
    TraceID: str
    # _trace_id: str
    compose_project: str
    compose_service: str
    container_name: str
    filename: str
    host: str
    latitude: str
    level: str
    longitude: str
    resource_service_name: str
    service_name: str
    source: str
    span_id: str

class LogData(BaseModel):
    logs: list[Log]

class AnomalyResponse(BaseModel):
    score: float
data = {
    "logs": [
    {
        "Time": "1727087298653",
        "Line": "2024-09-23 10:28:18,653 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 200, 'size': '30', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298653907865",
        "id": "1727087298653907865_b3c38a1f",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298637",
        "Line": "2024-09-23 10:28:18,637 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/forget_password', 'status': 200, 'size': '38', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298637828347",
        "id": "1727087298637828347_ce179337",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298622",
        "Line": "2024-09-23 10:28:18,622 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298622260282",
        "id": "1727087298622260282_8101baac",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298605",
        "Line": "2024-09-23 10:28:18,605 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298605900157",
        "id": "1727087298605900157_ad82dec5",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298590",
        "Line": "2024-09-23 10:28:18,590 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 200, 'size': '30', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298590948758",
        "id": "1727087298590948758_6822576b",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298576",
        "Line": "2024-09-23 10:28:18,576 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298576665816",
        "id": "1727087298576665816_8348c4fc",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298560",
        "Line": "2024-09-23 10:28:18,560 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298560586033",
        "id": "1727087298560586033_8a29c631",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298537",
        "Line": "2024-09-23 10:28:18,537 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/forget_password', 'status': 200, 'size': '38', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298537390019",
        "id": "1727087298537390019_eb9e6250",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298521",
        "Line": "2024-09-23 10:28:18,521 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298521514638",
        "id": "1727087298521514638_58076af8",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298499",
        "Line": "2024-09-23 10:28:18,498 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 200, 'size': '30', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298499102383",
        "id": "1727087298499102383_b5f7b202",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298484",
        "Line": "2024-09-23 10:28:18,483 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298484014362",
        "id": "1727087298484014362_91621209",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298469",
        "Line": "2024-09-23 10:28:18,468 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 200, 'size': '30', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298469159185",
        "id": "1727087298469159185_f5f98d7f",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298454",
        "Line": "2024-09-23 10:28:18,454 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298454383443",
        "id": "1727087298454383443_41e2875",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298439",
        "Line": "2024-09-23 10:28:18,438 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/forget_password', 'status': 200, 'size': '38', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298439250273",
        "id": "1727087298439250273_28f0b596",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298424",
        "Line": "2024-09-23 10:28:18,424 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298424582021",
        "id": "1727087298424582021_77c03320",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298410",
        "Line": "2024-09-23 10:28:18,409 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/forget_password', 'status': 200, 'size': '38', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298410116425",
        "id": "1727087298410116425_52153a8e",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298394",
        "Line": "2024-09-23 10:28:18,394 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298394932896",
        "id": "1727087298394932896_2cd144de",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298370",
        "Line": "2024-09-23 10:28:18,370 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 200, 'size': '30', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298370980053",
        "id": "1727087298370980053_948f1faf",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298355",
        "Line": "2024-09-23 10:28:18,355 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298355684503",
        "id": "1727087298355684503_f289c10f",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298339",
        "Line": "2024-09-23 10:28:18,339 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 200, 'size': '30', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298339401939",
        "id": "1727087298339401939_c47eb0ee",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298323",
        "Line": "2024-09-23 10:28:18,323 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 200, 'size': '30', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298323216332",
        "id": "1727087298323216332_d91aa86b",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298308",
        "Line": "2024-09-23 10:28:18,308 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/forget_password', 'status': 200, 'size': '38', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298308439359",
        "id": "1727087298308439359_68519c00",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298293",
        "Line": "2024-09-23 10:28:18,293 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298293748135",
        "id": "1727087298293748135_4f5127c0",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298256",
        "Line": "2024-09-23 10:28:18,256 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 200, 'size': '30', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298256251942",
        "id": "1727087298256251942_64d2ce5a",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298238",
        "Line": "2024-09-23 10:28:18,238 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298238565155",
        "id": "1727087298238565155_3e466d9",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298221",
        "Line": "2024-09-23 10:28:18,221 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298221901744",
        "id": "1727087298221901744_cdecfdbb",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298201",
        "Line": "2024-09-23 10:28:18,201 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298201227907",
        "id": "1727087298201227907_389445a5",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298183",
        "Line": "2024-09-23 10:28:18,183 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/forget_password', 'status': 200, 'size': '38', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298183345416",
        "id": "1727087298183345416_ca27efc9",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298158",
        "Line": "2024-09-23 10:28:18,158 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298158872550",
        "id": "1727087298158872550_1e61bf8c",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    },
    {
        "Time": "1727087298143",
        "Line": "2024-09-23 10:28:18,143 - [Lat: 1.3521, Lon: 103.8198] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 200, 'size': '30', 'user_agent': 'python-httpx/0.27.0'}",
        "tsNs": "1727087298143310053",
        "id": "1727087298143310053_b821f9cb",
        "TraceID": "0",
        "_trace_id": "0",
        "compose_project": "fyp-cyberguard",
        "compose_service": "login-app",
        "container_name": "fyp-cyberguard-login-app-1",
        "filename": "/var/log/docker/386f468687068205a7f88ae6faf6cb83d08db4984d9eff55aecad4b2437c5663/json.log",
        "host": "docker-desktop",
        "latitude": "1.3521",
        "level": "info",
        "longitude": "103.8198",
        "resource_service_name": "login-app]",
        "service_name": "fyp-cyberguard-login-app-1",
        "source": "stderr",
        "span_id": "0"
    }
]
}



try:
    if len(data.get("logs")) != 30:
        raise HTTPException(status_code=400, detail="Number of logs not 30")

    # log_df = pd.DataFrame(data.logs)
    processed_data = preprocess_dataframe(data.get("logs"))
    
    # print("Processed Data:")
    # print(processed_data.head())

    processed_data = create_dummy(processed_data)
    # print("Data after Creating Dummies:")
    # print(processed_data.head())
    # Define the filename of the saved model
    model_filename = 'autoencoder_model.pkl'

    # Load the trained Isolation Forest model from file
    # with open(model_filename, 'rb') as file:
    #     model = pickle.load(file)
    # Assuming model is defined elsewhere in your code
    model = keras.models.load_model("./autoencoder_model.keras")
    score = model.predict(processed_data)
    score = AnomalyResponse(score=score)
    print(score)
    # return {"hi":"hi"}

except HTTPException as http_exc:
    raise http_exc

except Exception as e:
    print(f"An error occurred: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")