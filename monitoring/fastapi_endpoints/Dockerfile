FROM python:3.10-slim

WORKDIR /app

COPY . .
# COPY ./locustfile.py /locustfile.py
# COPY ./run.sh /run.sh

RUN pip install -r requirements.txt

# USER root 
# RUN chmod +x /run.sh
EXPOSE 8000

# ENTRYPOINT ["/run.sh"]
CMD python main.py