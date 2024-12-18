import React, { useState, useEffect } from "react";

const fetchLogs = async (url) => {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch logs");
    }

    const jsonData = await response.json();

    if (jsonData.message === "No active alerts") {
      return [];
    }

    return jsonData || [];
  } catch (error) {
    console.error("Error fetching logs:", error);
    return [];
  }
};

const ActiveAlertsTable = () => {
  const [logs, setLogs] = useState([]);
  const [noAlertsMessage, setNoAlertsMessage] = useState("");

  useEffect(() => {
    const fetchAndSetLogs = async () => {
      const url = "http://localhost:8099/active_alerts";
      const logData = await fetchLogs(url);

      if (logData.length === 0) {
        setNoAlertsMessage("No active alerts");
      } else {
        setNoAlertsMessage("");
      }

      const reorderedLogs = logData.map((log) => ({
        Timestamp: log.logged_at,
        Country: log.country,
        Instance: log.instance,
        "Instance ID": log.instance_id,
        "App Name": log.app_name,
        "App ID": log.app_id,
        Metric: log.metric,
        Value: log.value,
        Threshold: log.threshold,
        Status: log.status,
      }));

      setLogs(reorderedLogs);
    };

    fetchAndSetLogs();
  }, []);

  const handleRowClick = (field, value, log) => {
    if (field === "App Name") {
      window.location.href = `http://localhost:3001/applications/${log["App ID"]}`;
    } else if (field === "Instance") {
      window.location.href = `http://localhost:3001/instance/${log["Instance ID"]}`;
    } else if (field === "Country") {
      window.location.href = `http://localhost:3001/countries/${value}`;
    }
  };

  const headers = logs.length > 0 ? Object.keys(logs[0]) : [];

  return (
    <div className="container mx-auto h-full w-full">
      {noAlertsMessage ? (
        <div className="text-center text-gray-500 my-8">
          <p>{noAlertsMessage}</p>
        </div>
      ) : (
        <div className="space-y-4 h-full">
          <div className="relative overflow-y-auto h-full border border-gray-700 rounded-b-lg">
            <table className="min-w-full table-fixed border-collapse">
              <thead className="sticky top-0 bg-gray-800 text-white">
                <tr>
                  {headers.map((header) => (
                    <th key={header} className="px-4 py-2 border-b text-left">
                      {header}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {logs.map((log, index) => (
                  <tr
                    key={index}
                    className={`cursor-pointer ${
                      log.Status === "Red" ? "bg-red-700 text-white" : "hover:bg-gray-700"
                    }`}
                  >
                    {headers.map((header) => (
                      <td
                        key={header}
                        className="px-4 py-2 border-b"
                        onClick={() => handleRowClick(header, log[header], log)}
                      >
                        {log[header]}
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

export default ActiveAlertsTable;