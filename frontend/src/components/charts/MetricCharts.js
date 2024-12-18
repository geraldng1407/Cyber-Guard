import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

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
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
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

const MetricCharts = ({ instance_id }) => {
  const [metricsData, setMetricsData] = useState([]);
  const [metricsValues, setMetricsValues] = useState({});

  useEffect(() => {
    const fetchAndUpdateMetrics = async () => {
      try {
        const appId = await fetchAppIdFromInstanceId(instance_id);
        if (!appId) {
          console.error("App ID could not be retrieved for the instance ID:", instance_id);
          return;
        }

        const url = `http://localhost:8088/metrics/app/${appId}/instance/${instance_id}`;
        const body = { time_from: "now-1m", time_to: "now" };
        const data = await fetchMetricsData(url, body);

        if (data.length > 0) {
          const newMetricsValues = {};

          data.forEach((metric) => {
            const [timestamps, values] = metric.data;
            const metricName = metric.Metric;

            if (!newMetricsValues[metricName]) {
              newMetricsValues[metricName] = [];
            }

            timestamps.forEach((time, index) => {
              newMetricsValues[metricName].push({
                time: new Date(time).toLocaleTimeString(),
                value: values[index],
              });
            });
          });

          setMetricsData(data);
          setMetricsValues((prevState) => ({
            ...prevState,
            ...newMetricsValues,
          }));
        }
      } catch (error) {
        console.error('Error fetching or processing metrics data:', error);
      }
    };

    fetchAndUpdateMetrics();
    const intervalId = setInterval(fetchAndUpdateMetrics, 5000);

    return () => clearInterval(intervalId);
  }, [instance_id]);

  const generateChartData = (metricName, dataset) => {
    return {
      labels: dataset.map((point) => point.time),
      datasets: [
        {
          label: metricName,
          data: dataset.map((point) => point.value),
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
        },
      ],
    };
  };

  const chartOptions = {
    maintainAspectRatio: false,
    scales: {
      x: { title: { display: true, text: 'Time' } },
      y: { title: { display: true, text: 'Value' } },
    },
    plugins: {
      legend: {
        labels: {
          fontSize: 14,
        },
      },
    },
  };

  return (
    <div
      style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '20px',
        justifyContent: 'center',
        padding: '10px',
      }}
    >
      {Object.entries(metricsValues).map(([metricName, dataset]) => (
        <div
          key={metricName}
          style={{
            height: '300px',
            width: '400px',
            border: '1px solid #ddd',
            borderRadius: '8px',
            padding: '10px',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
          }}
        >
          <h3 style={{ textAlign: 'center', marginBottom: '10px' }}>
            {metricName}
          </h3>
          <Line
            data={generateChartData(metricName, dataset)}
            options={chartOptions}
          />
        </div>
      ))}
    </div>
  );
};

export default MetricCharts;