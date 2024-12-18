import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
from utils import preprocess_dataframe, create_dummy
import requests
import tensorflow as tf
import numpy as np


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

# @app.post("/anomaly")
# async def test_anomaly(data: LogData):
#     try:
#         if len(data.logs) != 30:
#             raise HTTPException(status_code=400, detail="Number of logs not 30")

#         # log_df = pd.DataFrame(data.logs)
#         processed_data = preprocess_dataframe(data.logs)
        
#         # print("Processed Data:")
#         # print(processed_data.head())

#         processed_data = create_dummy(processed_data)
#         # print("Data after Creating Dummies:")
#         # print(processed_data.head())
#         # Define the filename of the saved model
#         model_filename = 'isolation_forest_model.pkl'

#         # Load the trained Isolation Forest model from file
#         with open(model_filename, 'rb') as file:
#             model = pickle.load(file)
#         # Assuming model is defined elsewhere in your code
#         score = model.decision_function(processed_data)
#         score = AnomalyResponse(score=score)
#         return score
#         # return {"hi":"hi"}
    
#     except HTTPException as http_exc:
#         raise http_exc
    
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/anomaly")
async def test_anomaly():
    url = 'http://metricsService:5000/login/logs'
    print("eneted")
    
    try:
        # Make the GET request to the endpoint
        response = requests.get(url)
        
        # Raise an exception for HTTP error codes
        response.raise_for_status()
        
        # Assuming the response is in JSON format
        logs = response.json()
        
#         logs = [
#     "2024-11-20 14:00:15,102 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54854 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:15,081 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54838 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:15,059 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54832 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:15,033 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54824 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,996 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54808 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,947 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54792 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,870 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54784 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,822 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54778 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,800 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54766 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,762 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54752 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,700 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54746 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,581 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54736 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,550 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54732 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,527 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54730 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,482 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54718 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,407 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54712 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,340 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54702 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,245 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54698 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,219 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54688 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,172 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54672 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,051 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54668 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,033 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54666 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:14,010 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54658 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:13,987 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54656 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:13,961 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54654 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:13,919 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54648 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:13,879 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54638 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:13,804 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54632 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:13,729 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54624 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:13,632 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54620 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:13,598 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54618 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:13,574 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54610 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:13,530 - [Lat: Unknown, Lon: Unknown] - INFO [uvicorn.access] [httptools_impl.py:481] [trace_id=0 span_id=0 resource.service.name=login-app] - 172.19.0.1:54608 - \"POST /login HTTP/1.1\" 401",
#     "2024-11-20 14:00:15,197 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=6c317b1e4c5adb4ab595652b731e70cc span_id=a718077ada689266 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:15,101 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:15,100 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=5d92d9cf81b08e323d57ed0a89552c5c span_id=1f726d75e01da879 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:15,081 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:15,080 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=4688bc6e411b2db8de8081568b34c2d3 span_id=9a7cc62bc6ac5d7c resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:15,059 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:15,057 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=e9e86c936f04b48252da4e5272873e87 span_id=53d0038c564111e8 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:15,032 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:15,031 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=fe8924823db21ae2db18b61003a2ee8a span_id=17bf436a2fbb9fb9 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,996 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,993 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=bbdf8f6ccdc30996d8513ba0d4b0fa67 span_id=52f680af74abd130 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,946 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,941 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=419ce1bce9a4003b06b4782e2f4897b0 span_id=f93f2b79995d8289 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,869 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,866 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=d5b03abe7a388ae9a1e7653de208c913 span_id=4487625f5cfef69a resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,822 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,821 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=afcf566308b40e4d932f4cd69497a83d span_id=9ddf3ee6589e8811 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,799 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,797 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=c2f79fa128dfe525b3deaa97f6fc6aba span_id=86a3c2fcfd64b509 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,762 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,760 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=bb83fc0e2df80c7584682ffc8f352136 span_id=ad724d8558febab7 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,699 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,694 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=df19d9e1b041e62e9586fcf5a002e61a span_id=77cf177ab2168302 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,580 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,578 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=75a5d8e19eb42afdff60ce1ed9308b44 span_id=fb1a0e6c104304fc resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,550 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,549 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=2df8de97df464e9fc92a46cd6ba71d7c span_id=99b179836f37065a resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,527 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,525 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=6dea8fcbd1b7b14fcca481f9e14592ad span_id=518a319bc7005a7a resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,481 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,477 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=34da58a37ef1f3b35c223ff171792c2e span_id=828a549b7781fe48 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,406 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,403 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=fcba927cfa61f15e763c4b614dbeadc2 span_id=858be54def129113 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,339 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,329 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=804b2aa355cc07cc6cb4f3a15aafce52 span_id=831fcecfb61de4dc resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,244 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,243 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=a0fc7efbdf619c0af874eb23e0b77227 span_id=36990e83afed958f resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,219 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,216 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=90cd566cacacaff60f12d84acd08ce03 span_id=27ef6fe60fa92607 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,167 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,164 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=311d22d96efc3ede50847d18dc756f45 span_id=3021b45ff925bb80 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,051 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,050 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=30b1c825027bdaf85d11d07458c157ed span_id=d39c5e482073ba92 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,032 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,032 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=0a99fd6dd587dba2b72afd0ebc1597fa span_id=021fa583a212351f resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:14,010 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:14,008 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=afc0bf0c9ba427dbfe1c53ea24e65a18 span_id=9a697c948238b0f4 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:13,986 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:13,986 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=213f103672fa015ad423fa824608e794 span_id=e975ad42aedd1b2f resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:13,961 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:13,957 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=144deae48abf06ebfafbd1a86d260a12 span_id=508f65ca4636004d resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:13,919 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:13,917 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=ede0fd591fc09097f91a9085a8656f06 span_id=0147fce1c094abf3 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:13,878 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:13,875 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=e181feee2a8007530bb3af7b98bbe64b span_id=f3de742347aa37d6 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:13,803 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:13,801 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=0cbddb2e737e6aa49aa15cca759388b3 span_id=4702d4c94de3dc13 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:13,728 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:13,720 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=69a0bccb761d4ca73cfed9dcd0281659 span_id=246bab1f18b43c75 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:13,631 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:13,631 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=ab175c2a2a0e00d7a23f6919707d8a28 span_id=2e14548dc8238d58 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:13,597 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:13,595 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=81c5280a325b74374551b04096b13e9d span_id=b7927c6c1c6eac7c resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:13,573 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:13,571 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=8bc6dd512104c428f67be2e4f2795872 span_id=39c8e34e60b35d86 resource.service.name=login-app] - Failed login attempt for user: johndoe",
#     "2024-11-20 14:00:13,529 - [Lat: Unknown, Lon: Unknown] - INFO [login-app] [main.py:115] [trace_id=0 span_id=0 resource.service.name=login-app] - Response - {'clientip': '192.168.0.1', 'method': 'POST', 'url': '/login', 'status': 401, 'size': '32', 'user_agent': 'python-httpx/0.27.0'}",
#     "2024-11-20 14:00:13,523 - [Lat: Unknown, Lon: Unknown] - ERROR [login-app] [main.py:132] [trace_id=c481052bd29e4612fcf6199ce8ae4f78 span_id=3bf1758559cd9387 resource.service.name=login-app] - Failed login attempt for user: johndoe"
# ]
        
        logs = [entry for entry in logs if "main.py" in entry]
        logs = logs[:30]

        processed_data = preprocess_dataframe(logs)
        
        processed_data = create_dummy(processed_data)

        processed_tensor = tf.convert_to_tensor(processed_data, dtype=tf.float32)
        try:
            # Load saved model directly
            model = tf.saved_model.load("saved_model")
            
            # Get prediction function
            pred_fn = model.signatures["serving_default"]
            
            # Debug available keys
            predictions = pred_fn(tf.constant(processed_tensor))
            print("Available keys:", predictions.keys())
            
            # Make prediction using correct key (usually 'dense' or similar)
            reconstructed_data = predictions[list(predictions.keys())[0]].numpy()
            
            # Calculate reconstruction error
            mse = np.mean(np.power(processed_data - reconstructed_data, 2), axis=1)
            
            score = AnomalyResponse(score=float(mse[0]))
            is_anomaly = score.score > 0.02
            
            return {
                "anomaly": is_anomaly
            }

        except Exception as model_error:
            print(f"Model loading/prediction error: {model_error}")
            raise HTTPException(status_code=500, detail="Model prediction failed")
    
    except HTTPException as http_exc:
        raise http_exc
