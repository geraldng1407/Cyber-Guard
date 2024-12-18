import React, { useState, useEffect } from 'react';

// Helper function to fetch logs
const fetchLogs = async (url, body) => {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch logs');
    }

    const jsonData = await response.json();

    const country = jsonData.Country || 'Unknown';
    const code = jsonData.Code || 'Unknown';
    
    const logsData = jsonData.Logs || [[], []];
    const [timeStamps, logMessages] = logsData;

    return {
      timeStamps,
      logMessages,
      country,
      code,
      instance: jsonData.Instance || 'Unknown'
    };
  } catch (error) {
    console.error('Error fetching logs:', error);
    return {
      timeStamps: [],
      logMessages: [],
      country: 'Unknown',
      code: 'Unknown',
      instance: 'Unknown'
    };
  }
};

const ApplicationInstanceLogsTable = ({ logsExpanded, instance_id }) => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true); 
  const [currentInstanceId, setCurrentInstanceId] = useState(instance_id);

  const fetchLogsData = async () => {
    try {
      const logData = await fetchLogs(`http://localhost:8088/logs/${instance_id}`, {
        "limit": "20", 
        "time_from": "now-1m", 
        "time_to": "now"
      });

      setLogs(() => {
        const newLog = {
          dateTime: new Date().toLocaleString(),
          ...logData
        };
        const updatedLogs = [newLog];
        sessionStorage.setItem('logs', JSON.stringify(updatedLogs));
        return updatedLogs;
      });
    } catch (error) {
      console.error('Error fetching logs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (instance_id !== currentInstanceId) {
      setCurrentInstanceId(instance_id);
      setLoading(true);
    }
    fetchLogsData();

    const intervalId = setInterval(fetchLogsData, 5000);
    return () => clearInterval(intervalId);
  }, [instance_id]);

  return (
    <div className="container mx-auto mt-8">
      {logsExpanded && (
        <div className="space-y-4">
          <div className="flex justify-between items-center bg-gray-800 p-4 rounded-t-lg">
            <div>
              <h2 className="text-white text-lg font-semibold">
                Instance: {logs[logs.length - 1]?.instance || 'Unknown'}
              </h2>
              <p className="text-gray-300">
                Location: {logs[logs.length - 1]?.country} ({logs[logs.length - 1]?.code})
              </p>
            </div>
            {/* Refresh Logs Button */}
            <button
              onClick={fetchLogsData}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded"
            >
              Refresh Logs
            </button>
          </div>
          {loading ? (
            <div className="text-center text-gray-300 text-lg">Loading...</div>
          ) : (
            <div className="relative overflow-y-auto h-96 border border-gray-700 rounded-b-lg">
              <table className="min-w-full table-fixed border-collapse">
                <thead className="sticky top-0 bg-gray-800 text-white">
                  <tr>
                    <th className="w-1/4 px-4 py-2 border-b border-gray-700 text-left">Timestamp</th>
                    <th className="w-3/4 px-4 py-2 border-b border-gray-700 text-left">Log Message</th>
                  </tr>
                </thead>
                <tbody className="bg-gray-900 text-gray-300">
                  {logs.slice(-5).map((logEntry, index) =>
                    logEntry.logMessages &&
                    logEntry.timeStamps &&
                    logEntry.logMessages.map((logMessage, idx) => (
                      <tr key={`${index}-${idx}`} className="hover:bg-gray-800">
                        <td className="px-4 py-2 border-b border-gray-700 break-words">
                          {logEntry.timeStamps[idx]}
                        </td>
                        <td className="px-4 py-2 border-b border-gray-700 break-words">
                          {logMessage}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ApplicationInstanceLogsTable;
