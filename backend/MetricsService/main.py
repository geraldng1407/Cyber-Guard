import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
from datetime import datetime, timezone
import mysql.connector
from urllib.parse import unquote

api_key = None
query_url = os.environ.get("QUERY_URL", "http://localhost:3000/api/ds/query")
query_headers = None
app = Flask(__name__)

CORS(app, origins=["http://localhost:3001"])

failed_response = {"message": "Failed to obtain metrics"}

db_password = os.getenv('MYSQL_ROOT_PASSWORD', 'password')
db_name = os.getenv('MYSQL_DATABASE', 'metrics_db')
db_user = os.getenv('DB_USER', 'root')
db_host = os.getenv('DB_HOST', 'metricsDatabase')

def get_db_connection():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return connection

def get_alerts(country):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT m.metric, i.instance_name, i.country, a.threshold FROM alerts a JOIN instances i ON a.instance_id = i.instance_id JOIN metrics m ON a.metric_id = m.metric_id WHERE i.country = %s", (country,))
    alerts = cursor.fetchall()
    cursor.close()
    connection.close()
    return alerts

@app.route('/countries', methods=['GET'])
def get_countries():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT country FROM instances")
    instances = cursor.fetchall()
    cursor.close()
    connection.close()
    country_list = [instance['country'] for instance in instances]
    return jsonify(country_list), 200

@app.route("/instances/<country>", methods=['GET'])
def get_instances_by_country(country):
    country = unquote(country)
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM instances, applications WHERE country = %s and instances.app_id = applications.app_id", (country,))
    instance = cursor.fetchall()
    cursor.close()
    connection.close()
    return instance


@app.route('/instances/get_name/<instance_id>', methods=['GET'])
def get_instance_name(instance_id):
    try:
        instance_name = get_instance_name_by_id(instance_id)
        if not instance_name:
            return jsonify({"error": "Instance not found", "instance_id": instance_id}), 404
        return jsonify({"instance_id": instance_id, "instance_name": instance_name}), 200
    except ValueError as ve:
        return jsonify({"error": "Invalid instance ID", "details": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/instances/get_app_id/<instance_id>', methods=['GET'])
def get_app_id(instance_id):
    try:
        app_id = get_app_id_by_instance_id(instance_id)
        if not app_id:
            return jsonify({"error": "App ID not found for the given instance", "instance_id": instance_id}), 404
        return jsonify({"instance_id": instance_id, "app_id": app_id}), 200
    except ValueError as ve:
        return jsonify({"error": "Invalid instance ID", "details": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route('/instances', methods=['GET'])
def get_instances():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""SELECT 
                        instances.*, applications.app_id, applications.app_name, applications.version_no, applications.provider, applications.release_date,
                        applications.build_no, applications.no_instances, applications.description, applications.saved
                        FROM instances
                        JOIN applications ON instances.app_id = applications.app_id """)
    instances = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(instances), 200

def get_instance_id(instance_name):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""SELECT 
                        instances.*, applications.app_id, applications.app_name, applications.version_no, applications.provider, applications.release_date,
                        applications.build_no, applications.no_instances, applications.description, applications.saved
                        FROM instances
                        JOIN applications ON instances.app_id = applications.app_id 
                        WHERE instances.instance_name = %s""", (instance_name, ))
    instance = cursor.fetchone()
    cursor.close()
    connection.close()
    return instance

def get_instance_name_by_id(instance_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    print(f"Fetching instance for ID: {instance_id}")
    cursor.execute("SELECT instance_name FROM instances WHERE instance_id = %s", (instance_id,))
    instance = cursor.fetchone()
    cursor.close()
    connection.close()
    return instance

def get_app_id_by_instance_id(instance_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT app_id FROM instances WHERE instance_id = %s", (instance_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result['app_id'] if result else None

def get_country_instances(country):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
            SELECT instance_id, instance_name, app_id
            FROM instances
            WHERE country = %s;
            """
    cursor.execute(query, (country,))
    instances = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(instances), 200

def post_request(query: str, time_from: str, time_to: str):
    headers = {"Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"}

    body = {"queries": [{
                "refId": "A",
                "datasource": {
                    "uid": "prometheus"
                },
                "format": "timeseries-multi",
                "intervalMs": 15000,
                "expr": query,
                "Step": "15s"}],
            "from": time_from,
            "to": time_to
        }
    
    response = requests.post(query_url, headers=headers, json=body)
    
    return response

def format_time(response):
    timestamps = []
    for ts in response:
        dt = datetime.fromtimestamp(ts / 1000.0)
        timestamps.append(dt)

    return timestamps

def format_response(response, metricName):
    metric = metricName
    country = response['schema']['fields'][1]['labels']['country']
    instance = response['schema']['fields'][1]['labels']['instance'].replace(":8000", "") 
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT m.metric, i.instance_name, i.country, a.threshold FROM alerts a JOIN instances i ON a.instance_id = i.instance_id JOIN metrics m ON a.metric_id = m.metric_id WHERE m.metric = %s AND i.instance_name = %s AND i.country = %s", (metric,instance, country))
    alert = cursor.fetchone()
    cursor.close()
    connection.close()

    flag=None
    threshold =None
    if alert:
        threshold = alert['threshold']
        flag = "Green"
        if metricName in ["Availability of database", "Availability of instance"]:
            if response['data']['values'][1][-1] < threshold:
                flag = "Red"
        else:
            if response['data']['values'][1][-1] > threshold:
                flag = "Red"
    
    instance_details = get_instance_id(instance)
    # return instance_details
    if not instance_details:
        return

    response_data = {"Metric": metricName,
                    "Instance": instance,
                    "Instance ID": instance_details['instance_id'],
                    "Country": country,
                    "Code": response['schema']['fields'][1]['labels']['code'],
                    "App ID": instance_details['app_id'],
                    "App Name": instance_details['app_name'],
                    "Build No": instance_details['build_no'],
                    "Description": instance_details['description'],
                    "No of Instances": instance_details['no_instances'],
                    "Provider": instance_details['provider'],
                    "Release date": instance_details['release_date'],
                    "Version No": instance_details['version_no'],
                    "Saved": instance_details['saved'],
                    "Threshold": threshold,
                    #data = [timestamp, values]
                    "Latest update": flag,
                    "data": [format_time(response['data']['values'][0]),
                            response['data']['values'][1]]}
    return response_data


@app.route('/applications', methods=['GET'])
def get_applications():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
            SELECT * FROM applications;
            """
    cursor.execute(query)
    instances = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(instances), 200

@app.route('/applications/<app_id>', methods=['GET'])
def get_app_instances(app_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = f"""
            SELECT a.app_id, a.app_name, a.version_no, a.provider, a.release_date, a.build_no, a.no_instances, a.description,
                ai.instance_id, ai.instance_name, ai.country, ai.code, a.saved
            FROM applications a
            LEFT JOIN instances ai ON a.app_id = ai.app_id
            WHERE a.app_id = {app_id};
            """
    cursor.execute(query)
    instances = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(instances), 200

@app.route('/applications/<app_id>/metrics', methods=['GET'])
def get_app_metrics(app_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = f"""
            SELECT * FROM app_metrics am LEFT JOIN metrics m on am.metric_id=m.metric_id WHERE app_id = {app_id};
            """
    cursor.execute(query)
    metrics = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(metrics), 200

@app.route('/applications/<app_id>/metrics/add', methods=['POST'])
def add_app_metrics(app_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    data = request.get_json()
    metric_id = data.get("metric_id")

    check_query = """
        SELECT COUNT(*) FROM app_metrics WHERE app_id = %s AND metric_id = %s
    """
    cursor.execute(check_query, (app_id, metric_id))
    result = cursor.fetchone()

    # return jsonify(result)
    if result['COUNT(*)'] != 0:
        return jsonify({"message": "Metric already exists for this app."}), 409  # Conflict

    insert_query = """
        INSERT INTO app_metrics (app_id, metric_id)
        VALUES (%s, %s)
    """
    try:
        cursor.execute(insert_query, (app_id, metric_id))
        connection.commit()
        message = {"message": f"Metric {metric_id} successfully added to app {app_id}."}
        status_code = 201  # Created
    except Exception as e:
        connection.rollback()
        message = {"error": str(e)}
        status_code = 400  # Bad Request
    cursor.close()
    connection.close()
    return jsonify(message), status_code

@app.route('/applications/<app_id>/metrics/delete', methods=['DELETE'])
def delete_app_metrics(app_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    data = request.get_json()
    metric_id = data.get("metric_id")

    delete_query = """
        DELETE FROM app_metrics
        WHERE app_id = %s AND metric_id = %s
    """
    try:
        cursor.execute(delete_query, (app_id, metric_id))
        connection.commit()
        if cursor.rowcount > 0:
            message = {"message": f"Metric {metric_id} successfully removed from app {app_id}."}
            status_code = 200  # OK
        else:
            message = {"error": "No matching record found to delete."}
            status_code = 404  # Not Found
    except Exception as e:
        connection.rollback()
        message = {"error": str(e)}
        status_code = 400  # Bad Request
    finally:
        cursor.close()
        connection.close()
    return jsonify(message), status_code


@app.route('/<country>', methods=['GET'])
def get_country_alerts_count(country):
    country = unquote(country)
    try:  
        response = requests.post(f'http://metricsService:5000/metrics/{country}', 
                                    headers={"Content-Type": "application/json"},
                                    json={"interval": "1m", "time_from":"now-5m", "time_to":"now"})
        current_metrics = response.json()

        # country_alerts = get_alerts(country)
        alerts_count = 0
        alerts_instance = {}
        
        response = {}

        code = current_metrics[0]['Code']
        timestamps = current_metrics[0]['data'][0]
        latest_timestamp = timestamps[-1]
        response["Last Updated"] = latest_timestamp

        for data in current_metrics:
            metric = data['Metric']
            instance = data['Instance']

            if data['Latest update'] == 'Red':
                alerts_count += 1
                instance_count = alerts_instance.setdefault(instance, 0)
                alerts_instance[instance] = instance_count + 1

        response["Country"] = country
        response["Code"] = code
        response["Number of alerts flagged in total"] = alerts_count
        response["Number of instances flagged"] = len(alerts_instance)

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch country metrics', 'message': str(e)}), 400



def get_all_metrics_instances(data, instances, metrics_list):
    time_from = data.get('time_from', 'now-5m')  # Default to 'now-5m' if not provided
    time_to = data.get('time_to', 'now')
    interval = data.get('interval', '1m')
    instance_string = "|".join(instances)

    
    metrics = {'Memory usage for instance': f'process_resident_memory_bytes{{instance=~"{instance_string}"}} / 1024 ^ 2',
             'CPU utilization for instance': f'rate(process_cpu_seconds_total{{instance=~"{instance_string}"}}[{interval}]) * 100',
             'Rate of slow queries': f'rate(mysql_global_status_slow_queries{{instance=~"{instance_string}"}}[{interval}])',
             'Rate of connection errors': f'rate(mysql_global_status_connection_errors_total{{instance=~"{instance_string}"}}[{interval}])',
             'Percentage of available connections used': f'100 * mysql_global_status_threads_connected{{instance=~"{instance_string}"}} / mysql_global_variables_max_connections{{instance=~"{instance_string}"}}',
             'Availability of database': f'mysql_up{{instance=~"{instance_string}"}}',
             'Traffic for delete operations': f'rate(mysql_global_status_innodb_row_ops_total{{instance=~"{instance_string}", operation="deleted"}}[{interval}])',
             'Traffic for read operations': f'rate(mysql_global_status_innodb_row_ops_total{{instance=~"{instance_string}", operation="read"}}[{interval}])',
             'Traffic for insert operations': f'rate(mysql_global_status_innodb_row_ops_total{{instance=~"{instance_string}", operation="inserted"}}[{interval}])',
             'Traffic for update operations': f'rate(mysql_global_status_innodb_row_ops_total{{instance=~"{instance_string}", operation="updated"}}[{interval}])',
            #  f'sum(rate(http_requests_total{{country="{country}", status=~"4..|5.."}}[{interval}])) by (handler, instance, container_name, job, latitude, longitude) /sum(rate(http_requests_total{{country="{country}"}}[{interval}])) by (handler, instance, container_name, job, latitude, longitude)',
             'Error rate for instance': f'sum(rate(http_requests_total{{instance=~"{instance_string}", status=~"4..|5.."}}[{interval}])) by (instance, job, country, code)/sum(rate(http_requests_total{{instance=~"{instance_string}"}}[{interval}])) by (instance, job, country, code)',
             'Traffic for instance': f'sum(rate(http_requests_total{{instance=~"{instance_string}"}}[{interval}])) by (instance, job, country, code)',
             'Availability of instance': f'(sum(rate(http_requests_total{{instance=~"{instance_string}",status="2xx"}}[{interval}])) by (instance, job, country, code) * 100) / sum(rate(http_requests_total{{instance=~"{instance_string}"}}[{interval}])) by (instance, job, country, code)',
            #  f'(sum(rate(http_request_duration_seconds_sum{{country="{country}"}}[{interval}])) by (handler, instance, container_name, job, latitude, longitude))  / sum(rate(http_request_duration_seconds_count{{country="{country}"}}[{interval}])) by (handler, instance, container_name, job, latitude, longitude)',
             'Latency of instance': f'sum(rate(http_request_duration_seconds_sum{{instance=~"{instance_string}"}}[{interval}])) by (instance, job, country, code) / sum(rate(http_request_duration_seconds_count{{instance=~"{instance_string}"}}[{interval}])) by (instance, job, country, code)',
             'Traffic for 2xx': f'sum(rate(http_requests_total{{instance=~"{instance_string}", status="2xx"}}',
             'Traffic for 4xx': f'sum(rate(http_requests_total{{instance=~"{instance_string}", status="4xx"}}'}

    query_list = []
    final_metrics = []
    for metric in metrics_list:
        query_list.append(metrics[metric["metric"]])
        final_metrics.append(metric["metric"])

    queries = []
    for index in range(len(query_list)):
        query = {
                "refId": str(index),
                "datasource": {
                    "uid": "prometheus"
                },
                "format": "timeseries-multi",
                "intervalMs": 15000,
                "expr": query_list[index],
                "Step": "15s"}
        
        queries.append(query)

    headers = {"Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"}
    body = {"queries": queries,
            "from": time_from,
            "to": time_to
        }

    try:
        response = requests.post(query_url, headers=headers, json=body)
        response = response.json()

        responses = []
        # return jsonify(response), 200
        for key, result in response['results'].items():
            for frame in result['frames']:
                if frame['data']['values'] == []:
                    continue
                index = int(key)
                metric = final_metrics[index]

                response_data = format_response(frame, metric)
                if not response_data:
                    continue
                responses.append(response_data)

        return jsonify(responses), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch metrics', 'message': str(e)}), 400

@app.route('/metrics/<country>', methods=['POST'])
def get_country_metrics(country):
    data = request.json
    country = unquote(country)
    country_instances, status_code = get_country_instances(country)
    country_instances = country_instances.get_json()
    # return jsonify(country_instances)
    responses = []
    for instance in country_instances:
        # return jsonify(instance)
        instance_name = instance['instance_name']+ ":8000"
        app_id = instance['app_id']
        instance_id = instance['instance_id']
        metrics_response, status_code = get_app_metrics(app_id)
        metrics = metrics_response.get_json()
        response, status_code = get_all_metrics_instances(data, [instance_name], metrics)
        if status_code == 200:
            response = response.get_json()
            # return jsonify(response)
            responses.extend(response)

    return responses

#get all metrics for a application
@app.route('/metrics/app/<app_id>', methods=['POST'])
def get_metrics_apps(app_id):
    data = request.json
    app_instances, status_code = get_app_instances(app_id)
    app_instances = app_instances.get_json()
    instances = [instance['instance_name']+ ":8000" for instance in app_instances]
    metrics_response, status_code = get_app_metrics(app_id)
    metrics = metrics_response.get_json()

    return get_all_metrics_instances(data, instances, metrics)

@app.route('/metrics/app/<app_id>/instance/<instance_id>', methods=['POST'])
def get_app_instance_metric(app_id, instance_id):
    data = request.json
    instance = get_instance_name_by_id(instance_id)['instance_name'] + ":8000"
    metrics_response, status_code = get_app_metrics(app_id)
    metrics = metrics_response.get_json()

    return get_all_metrics_instances(data, [instance], metrics)

#get saved applications
@app.route('/saved/app', methods=['GET'])
def get_saved_applications():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
            SELECT * FROM applications WHERE saved = 1;
            """
    cursor.execute(query)
    instances = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(instances), 200

@app.route('/saved/app/<app_id>', methods=['PUT'])
def toggle_saved_app(app_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    check_query = "SELECT saved FROM applications WHERE app_id = %s;"
    cursor.execute(check_query, (app_id,))
    app = cursor.fetchone()

    if not app:
        cursor.close()
        connection.close()
        return jsonify({"message": f"Application with ID {app_id} not found."}), 404

    current_saved_value = app['saved']
    new_saved_value = 0 if current_saved_value == 1 else 1

    update_query = "UPDATE applications SET saved = %s WHERE app_id = %s;"
    cursor.execute(update_query, (new_saved_value, app_id))
    connection.commit()

    cursor.close()
    connection.close()

    if new_saved_value == 1:
        message = f"Application with ID {app_id} has been marked as saved."
    else:
        message = f"Application with ID {app_id} has been marked as unsaved."

    return jsonify({"message": message}), 200


###mock set alert
@app.route('/alerts/set_threshold', methods=['POST'])
def set_threshold():
    data = request.json
    metric = data.get('metric', None)
    country = data.get('country', None)
    instance_name = data.get('instance', None)
    new_threshold = data.get('threshold', None)

    if metric == None or country == None or instance_name == None or new_threshold == None:
        return jsonify({"Error": "Request error"}), 400
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("UPDATE alerts a JOIN instances i ON a.instance_id = i.instance_id JOIN metrics m ON a.metric_id = m.metric_id SET a.threshold = %s WHERE i.country = %s AND i.instance_name = %s AND m.metric = %s;", (int(new_threshold), country, instance_name, metric))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"Response": "Update completed"}), 200
    except Exception as e:
        return jsonify({'Error': 'Failed to set threshold', 'message': str(e)}), 400

@app.route('/alerts/add_alert', methods=['POST'])
def add_alert():
    data = request.json
    metric = data.get('metric', None)
    country = data.get('country', None)
    instance_name = data.get('instance', None)
    threshold = data.get('threshold', None)

    if metric == None or country == None or instance_name == None or threshold == None:
        return jsonify({"Error": "Request error"}), 400
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            INSERT INTO alerts (metric_id, instance_id, threshold)
            SELECT m.metric_id, i.instance_id, %s
            FROM metrics m
            JOIN instances i ON i.instance_name = %s AND i.country = %s
            WHERE m.metric = %s;
            """, 
            (int(threshold), instance_name, country, metric)
        )
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"Response": "Alert added"}), 200
    except Exception as e:
        return jsonify({'Error': 'Failed to set threshold', 'message': str(e)}), 400

@app.route('/alerts', methods=['GET'])
def get_current_alerts():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT m.metric, i.instance_name, i.country, a.threshold FROM alerts a JOIN instances i ON  a.instance_id = i.instance_id JOIN metrics m ON a.metric_id = m.metric_id;")
    alerts = cursor.fetchall()
    cursor.close()
    connection.close()
    if alerts:
        return jsonify(alerts), 200
    return jsonifiy({'Error': 'No alerts retrieved'}), 400



@app.route('/metrices', methods=['GET'])
def get_metrics_name():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM metrics")
    alerts = cursor.fetchall()
    cursor.close()
    connection.close()
    if alerts:
        return jsonify(alerts), 200
    return jsonifiy({'Error': 'No metrics retrieved'}), 400


@app.route('/logs/<instance_id>', methods=['POST'])
def get_logs_instance(instance_id):
    data = request.json
    return get_logs(data, instance_id)

def get_logs(data, instance_id):
    instance_name = get_instance_name_by_id(instance_id)['instance_name']
    instance_details = get_instance_id(instance_name)
    compose_service = instance_name.split(':')[0]
    limit = data.get("limit", "500") 
    start = data.get("start_time", "now-120m")
    end = data.get("end_time", "now")

    query = f'{{compose_service="{compose_service}"}} |= ``'

    headers = {"Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"}

    body = {"queries": [{
                "refId": "A",
                "datasource": {
                    "uid": "loki"
                },
                "intervalMs": 15000,
                "expr": query,
                "Step": "15s"}],
            "from": start,
            "to": end,
            "maxLines": limit
        }
    
    response = requests.post(query_url, headers=headers, json=body)

    if response.status_code == 200:
        response = response.json()

        if response['results']['A']['frames'][0]['data']['values'][0] == []:
            return jsonify({"error": "no logs found"}), 400

        instance = response['results']['A']['frames'][0]['data']['values'][0][0]['compose_service']
        # timestamps = response['results']['A']['frames'][0]['data']['values'][1]
        timestamps = [convert_from_unix_nanos(ts) for ts in response['results']['A']['frames'][0]['data']['values'][1]]
        logs = response['results']['A']['frames'][0]['data']['values'][2]
        
        response_data = {"Instance": instance,
                         "Instance ID": instance_id,
                         "Country": instance_details['country'],
                         "Code": instance_details['code'],
                         "App ID": instance_details['app_id'],
                        "App Name": instance_details['app_name'],
                        "Build No": instance_details['build_no'],
                        "Description": instance_details['description'],
                        "No of Instances": instance_details['no_instances'],
                        "Provider": instance_details['provider'],
                        "Release date": instance_details['release_date'],
                        "Version No": instance_details['version_no'],
                        "Saved": instance_details['saved'],
                        "Logs": [timestamps, logs]}
        
        return jsonify(response_data), 200
    else:
        return jsonify({"error": response.text}), response.status_code


@app.route('/traces/<app_id>', methods=['GET'])
def get_traces_app(app_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applications WHERE app_id = %s", (app_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    app_name = result['app_name']
    headers = {"Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"}
    tempo_url = os.environ.get("TEMPO_URL", "http://host.docker.internal:3000/api/datasources/proxy/uid/tempo/")
    query_url = f"{tempo_url}api/search?q=%7Bresource.service.name%3D%22{app_name}%22%7D&limit=50&spss=5"
    response = requests.post(query_url, headers=headers)

    return response.json(), 200

@app.route('/traces', methods=['GET'])
def get_traces():
    headers = {"Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"}
    tempo_url = os.environ.get("TEMPO_URL", "http://host.docker.internal:3000/api/datasources/proxy/uid/tempo/")
    query_url = f"{tempo_url}api/search?limit=50&spss=5"
    response = requests.post(query_url, headers=headers)

    return response.json(), 200

    
def convert_from_unix_nanos(unix_nanos):
    if unix_nanos is None:
        return None
    try:
        # Convert nanoseconds to seconds
        unix_seconds = unix_nanos / 1000
        # Create a datetime object from the Unix timestamp
        utc_time = datetime.fromtimestamp(unix_seconds, tz=timezone.utc)
        # Return the formatted UTC time string
        return utc_time.strftime("%Y-%m-%d %H:%M:%S.%f")  # Adjust the format as needed
    except (TypeError, ValueError):
        return None  # Handle invalid input


@app.route('/login/logs', methods=['GET'])
def get_login_logs():

    query = f'{{container_name="monitoring-login-app-1"}} |= ``'

    headers = {"Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"}

    body = {"queries": [{
                "refId": "A",
                "datasource": {
                    "uid": "loki"
                },
                "intervalMs": 15000,
                "expr": query,
                "Step": "15s"}],
            "from": "now-1h",
            "to": "now",
            "maxLines": 1000}
    
    response = requests.post(query_url, headers=headers, json=body)

    if response.status_code == 200:
        response = response.json()

        if response['results']['A']['frames'][0]['data']['values'][0] == []:
            return jsonify({"error": "no logs found"}), 400

        logs = response['results']['A']['frames'][0]['data']['values'][2]
        return jsonify(logs), 200
    else:
        return jsonify({"error": response.text}), response.status_code



@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "service is healthy"}), 200

    
def load_api_key():
    if os.path.exists('/app/config/config.json'):
        with open('/app/config/config.json', 'r') as config_file:
            config = json.load(config_file)
            return config.get("key")
    return None

def create_apikey():
    global api_key
    api_key = load_api_key()

    if api_key:
        print("API Key already exists:", api_key)
        return

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "name": "admin_api_key", 
        "role": "Viewer"
    }
    response = requests.post("http://admin:admin@host.docker.internal:3000/api/auth/keys", headers=headers, json=body)

    if response.status_code == 200:
        # Assuming the response contains the API key in the expected format
        data = response.json()
        print(data)
        api_key = data.get("key")  # Update the global variable
        print("API Key fetched:", api_key)
        with open('/app/config/config.json', 'w') as config_file:
            json.dump(data, config_file)
    else:
        print("Failed to fetch API Key:", response.status_code, response.text)
    
def delete_config_file():
        file_path = '/app/config/config.json'
        
        # Check if the file exists
        if os.path.exists(file_path):
            try:
                # Delete the file
                os.remove(file_path)
                print(f"File '{file_path}' has been deleted.")
            except Exception as e:
                print(f"An error occurred while deleting the file: {e}")
        else:
            print(f"File '{file_path}' does not exist.")

if __name__ == '__main__':
    # delete config.json if exists 
    # delete_config_file()
    create_apikey()
    app.run(host= '0.0.0.0', port=5000, debug=True)
    