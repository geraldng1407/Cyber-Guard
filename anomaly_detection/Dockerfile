FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --default-timeout=100 -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

# FROM python:3.10-slim

# WORKDIR /app

# # Copy requirements and install dependencies first for better caching
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# # Copy saved model directory
# COPY saved_model ./saved_model/

# # Copy remaining application files
# COPY . .

# EXPOSE 8080

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
