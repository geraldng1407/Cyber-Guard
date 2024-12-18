import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
from datetime import datetime, timezone
import mysql.connector
import threading
import time

app = Flask(__name__)
CORS(app, origins=["http://localhost:3001"])
active_alerts = []

########################################
# notifications db
db_password = os.getenv('MYSQL_ROOT_PASSWORD', 'password')
db_name = os.getenv('MYSQL_DATABASE', 'notifications_db')
db_user = os.getenv('DB_USER', 'root')
db_host = os.getenv('DB_HOST', 'notificationsDatabase')


def get_db_connection():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return connection

def convert_datetime_fields(alert):
    # Loop through the fields and convert any datetime objects to string
    for key, value in alert.items():
        if isinstance(value, datetime):
            alert[key] = value.isoformat()  # Convert datetime to ISO 8601 format
    return alert

def get_countries():
    url = "http://metricsService:5000/countries"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch countries. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/slack', methods=['GET'])
def get_slack():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM slack")
    slack_info = cursor.fetchall()
    cursor.close()
    connection.close()
    return slack_info

def send_slack(blocks):
    headers={"Content-Type": "application/json"}
    message = {
                    "text": "Test text",
                    "blocks": blocks
                }

    #get slack webhooks
    slack_info = get_slack()
    for info in slack_info:
        channel = info['channel_name']
        workspace = info['workspace_name']
        webhook = info['webhook_url']
        try:
            response = requests.post(webhook,headers=headers,data=json.dumps(message))
        except Exception as e:
            return jsonify({"message": f"Error posting slack message to {channel} in {workspace}"}), 400

    return jsonify({"message": f"Slack message posted."}), 200

def save_alerts_to_redis(alerts):
    print("alerts saved")
    print(alerts)
    redis_client.set('active_alerts', json.dumps(alerts))

def load_alerts_from_redis():
    data = redis_client.get('active_alerts')
    return json.loads(data) if data else []

def log_data(current_metrices):
    # cache.delete('active_alerts')
    global active_alerts
    alerts = []
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    for value in current_metrices:
        # return jsonify(value)
        latest_value = value["data"][1][-1]
        cursor.execute("""INSERT INTO metrics_logs (metric, instance, instance_id, country, code, app_id, app_name, status, value, threshold) VALUES 
                       (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                       (value["Metric"], value["Instance"], value["Instance ID"], value["Country"], value["Code"], value["App ID"], value["App Name"], value["Latest update"], latest_value, value["Threshold"]))
        connection.commit()
        if value["Latest update"]=="Red":
            last_id = cursor.lastrowid
            cursor.execute("SELECT * FROM metrics_logs WHERE id = %s", (last_id,))
            inserted_row = cursor.fetchone()
            alerts.append(inserted_row)

    active_alerts = alerts
    connection.commit()
    cursor.close()
    connection.close()

    return

@app.route('/sendslack', methods=['GET'])
def check_thresholds():

    country_list = get_countries()
    blocks = []
    
    detailed_list = []
    alert_count = 0
    text = []
    data_to_log = []
    for country in country_list:
        #Latest flag updates
        response = requests.get(f"http://metricsService:5000/{country}")
        data = response.json()

        number_alerts = data.get('Number of alerts flagged in total', 0)

        response = requests.post(f'http://metricsService:5000/metrics/{country}', 
                        headers={"Content-Type": "application/json"},
                        json={"interval": "1m", "time_from":"now-5m", "time_to":"now"})
        current_metrics = response.json()
        data_to_log.extend(current_metrics)
        if number_alerts > 0:
            detailed_list.append(country)

            if alert_count == 0:
                header = {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": f"Alerts overview\nLast Updated: {data.get('Last Updated')}\n\n"
                            }
                        }
                blocks.append(header)
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "<http://localhost:3001/ | View dashboard>"
                    }
                })
                

            elements = [{
                            "type": "text",
                            "text": f"{data.get('Country')}\n",
                            "style": {"bold": True}
                        },
                        {
                            "type": "text",
                            "text": f"Number of alerts flagged in total: {number_alerts}      Number of instances flagged: {data.get('Number of instances flagged')}\n\n"
                        },
                        {
                            "type": "text",
                            "text": f"Alerts:\n"
                        },
                        ]

            for value in current_metrics:
                if value.get("Latest update") == "Red":
                    metric = value["Metric"]
                    instance = value["Instance"]
                    elements.append({
                                        "type": "text",
                                        "text": f'Metric "{metric}" for instance "{instance}"\n'
                                    })
            elements.append({
                                "type": "text",
                                "text": f'\n'
                            })

            blocks.append({
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": elements
                    }
                ]
            })

            blocks.append({
                "type": "divider"
            })

            alert_count += 1
    
    log_data(data_to_log)
    if alert_count == 0:
        header = {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Alerts overview\nLast Updated: {data.get('Last Updated')}"
                    }
                }
        blocks.append(header)
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "<http://localhost:3001/ | View dashboard>"
            }
        })
        block = {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": 'No alerts currently'
                        }
                    }
        blocks.append(block)

    
    response = requests.post(f'http://anomaly-detector:8080/anomaly')
    anomaly = response.json()

    if anomaly.get('anomaly') is True:
        header = {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Anomaly Alert: Anomaly detected on system"
            }
        }
        blocks.append(header)
        blocks.append({
                "type": "divider"
            })
    
    return send_slack(blocks)

@app.route('/anomalyalert', methods=['GET'])
def send_anomaly():
    block = {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": f"Anomaly Alert: Anomaly detected on system"
        }
    }
    return send_slack(block)

@app.route('/active_alerts', methods=['GET'])
def get_active_alerts():
    if active_alerts == []:
        return jsonify({"message": "No active alerts"}), 404
    return jsonify(active_alerts), 200

@app.route('/active_alerts/<id>', methods=['DELETE'])
def delete_active_alerts(id):
    global active_alerts

    try:
        alert_to_delete = next((alert for alert in active_alerts if alert["id"] == int(id)), None)

        if alert_to_delete:
            active_alerts.remove(alert_to_delete)
            return jsonify({"message": f"Alert with id {id} has been deleted."}), 200

        return jsonify({"message": f"No alert found with id {id}"}), 404
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

@app.route('/alerts_logs/all', methods=['GET'])
def get_logs():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM metrics_logs")
    logs = cursor.fetchall()
    cursor.close()
    connection.close()
    return logs

@app.route('/alerts_logs/red', methods=['GET'])
def get_logs_red():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM metrics_logs where status = 'Red'")
    logs = cursor.fetchall()
    cursor.close()
    connection.close()
    return logs

def check_thresholds_continuous(interval=300):
    while True:
        with app.app_context():
            check_thresholds()
        time.sleep(interval)

if __name__ == '__main__':
    interval_seconds = 300  # Set the interval to 5 minutes (300 seconds)
    background_thread = threading.Thread(target=check_thresholds_continuous, args=(interval_seconds,))
    background_thread.daemon = True  # Set as a daemon so it exits when the main thread does
    background_thread.start()
   
    app.run(host= '0.0.0.0', port=5000, debug=False)
