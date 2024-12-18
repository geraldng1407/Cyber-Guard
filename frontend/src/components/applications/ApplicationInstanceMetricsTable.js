import React, { useState, useEffect } from "react";

// Fetch active alerts
const fetchActiveAlerts = async () => {
  try {
    const response = await fetch("http://localhost:8099/active_alerts");
    if (!response.ok) {
      throw new Error("Failed to fetch active alerts");
    }
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching active alerts:", error.message);
    return [];
  }
};

// Fetch app_id from instance_id
const fetchAppIdFromInstanceId = async (instanceId) => {
  try {
    const response = await fetch(`http://localhost:8088/instances/get_app_id/${instanceId}`);
    if (!response.ok) {
      throw new Error("Failed to fetch app_id");
    }
    const jsonData = await response.json();
    return jsonData.app_id;
  } catch (error) {
    console.error("Error fetching app_id:", error);
    return null;
  }
};

// Fetch metrics data
const fetchMetricsData = async (url, body) => {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to fetch metrics: ${errorText}`);
    }

    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching metrics data:", error.message);
    return [];
  }
};

const ApplicationInstanceMetricsTable = ({ metricsExpanded, instance_id, instanceName }) => {
  const [metrics, setMetrics] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [activeAlerts, setActiveAlerts] = useState([]);

  const fetchAndProcessMetrics = async () => {
    try {
      const appId = await fetchAppIdFromInstanceId(instance_id);
      if (!appId) {
        console.error("App ID could not be retrieved for the instance ID:", instance_id);
        return;
      }

      // Fetch metrics
      const url = `http://localhost:8088/metrics/app/${appId}/instance/${instance_id}`;
      const body = { time_from: "now-1m", time_to: "now" };
      const data = await fetchMetricsData(url, body);

      if (data.length > 0) {
        const dynamicHeaders = ["DateTime", ...data.map((metric) => metric.Metric)];
        setHeaders(dynamicHeaders);

        const timestamps = data[0].data[0];
        const rows = timestamps.map((timestamp, index) => {
          const row = [timestamp, ...data.map((metric) => metric.data[1][index])];
          return row;
        });

        setMetrics(rows);
      }

      // Fetch active alerts and filter by instance_id
      const alerts = await fetchActiveAlerts();
      const alertsForInstance = alerts.filter((alert) => alert.instance_id === instance_id);
      setActiveAlerts(alertsForInstance);
    } catch (error) {
      console.error("Error during metrics fetch and processing:", error);
    }
  };

  useEffect(() => {
    if (metricsExpanded) {
      fetchAndProcessMetrics();
    }
  }, [metricsExpanded, instance_id, instanceName]);

  return (
    <div className="container mx-auto mt-8">
      {metricsExpanded && (
        <div className="space-y-4">
          <div className="flex justify-between items-center bg-gray-800 p-4 rounded-t-lg">
            <h2 className="text-white text-lg font-semibold">Instance: {instanceName}</h2>
            <button
              onClick={fetchAndProcessMetrics}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded"
            >
              Refresh Metrics
            </button>
          </div>
          <div className="relative overflow-y-auto h-64 border border-gray-700 rounded-b-lg">
            <table className="min-w-full table-fixed border-collapse">
              <thead className="sticky top-0 bg-gray-800 text-white">
                <tr>
                  {headers.map((header, index) => (
                    <th key={index} className="px-4 py-2 border border-gray-700">
                      {header}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {/* Render Active Alerts */}
                {activeAlerts.map((alert, index) => {
                  console.log(alert)

                  const alertRow = Array(headers.length).fill("");

                  alertRow[0] = alert.logged_at;

                  const metricIndex = headers.indexOf(alert.metric);

                  if (metricIndex !== -1) {
                    alertRow[metricIndex] = (
                      <>
                        <div>{alert.value}</div>
                        <div className="text-sm italic text-gray-200">Threshold: {alert.threshold}</div>
                      </>
                    );
                  }

                  return (
                    <tr key={index} className="bg-red-500 text-white">
                      {alertRow.map((cell, cellIndex) => (
                        <td key={cellIndex} className="px-4 py-2 border border-gray-700">
                          {cell || ""}
                        </td>
                      ))}
                    </tr>
                  );
                })}
              </tbody>
              <tbody>
                {/* Render Metrics */}
                {metrics.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {row.map((cell, cellIndex) => (
                      <td key={cellIndex} className="border px-4 py-2">
                        {cell}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default ApplicationInstanceMetricsTable;
