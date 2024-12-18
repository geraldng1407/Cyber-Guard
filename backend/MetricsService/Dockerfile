FROM python:3.10-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY wait-for-it.sh /usr/local/bin/wait-for-it

RUN chmod +x /usr/local/bin/wait-for-it

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["wait-for-it", "metricsDatabase:3306", "--timeout=60", "--"]

CMD ["python", "main.py"]
