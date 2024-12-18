import React, { useState, useEffect } from "react";
export default function Settings() {
    const [apps, setApps] = useState([]);
    const [alerts, setAlerts] = useState([]);
    const [instances, setInstances] = useState([]);
    const [metrics, setMetrics] = useState([]);
    const [selectedApp, setSelectedApp] = useState(null);
    const [selectedAppName, setSelectedAppName] = useState("");
    const [selectedCountry, setSelectedCountry] = useState(null);
    const [thresholds, setThresholds] = useState({});
  
    // Fetch apps
    useEffect(() => {
      const fetchApps = async () => {
        try {
          const response = await fetch(`http://localhost:8088/applications`);
          if (!response.ok) throw new Error("Failed to fetch applications");
          const appData = await response.json();
          setApps(appData);
        } catch (error) {
          console.error("Error fetching applications:", error);
        }
      };
  
      fetchApps();
    }, []);
  
    // Fetch alerts
    useEffect(() => {
      const fetchAlerts = async () => {
        try {
          const response = await fetch(`http://localhost:8088/alerts`);
          if (!response.ok) throw new Error("Failed to fetch alerts");
          const alertData = await response.json();
          setAlerts(alertData);
  
          const initialThresholds = {};
          alertData.forEach((alert) => {
            const key = `${alert.instance_name}-${alert.metric}`;
            initialThresholds[key] = alert.threshold;
          });
          setThresholds(initialThresholds);
        } catch (error) {
          console.error("Error fetching alerts:", error);
        }
      };
  
      fetchAlerts();
    }, []);
  
    // Fetch instances
    useEffect(() => {
      const fetchInstances = async () => {
        try {
          const response = await fetch(`http://localhost:8088/instances`);
          if (!response.ok) throw new Error("Failed to fetch instances");
          const instanceData = await response.json();
          setInstances(instanceData);
        } catch (error) {
          console.error("Error fetching instances:", error);
        }
      };
  
      fetchInstances();
    }, []);
  
    // Get instance_name for selected app and country
    const getInstanceName = (country, appId) => {
      const instance = instances.find(
        (instance) =>
          instance.country === country && instance.app_id === Number(appId)
      );
      return instance ? instance.instance_name : null;
    };

    const filteredAlerts = alerts.filter(
        (alert) =>
          alert.country === selectedCountry &&
          alert.instance_name === getInstanceName(selectedCountry, selectedApp)
    );      
  
    // Handle app change
    const handleAppChange = (appId) => {
      setSelectedApp(appId);
      const app = apps.find((app) => app.app_id === parseInt(appId));
      setSelectedAppName(app?.app_name || "");
    };

    // Update threshold dynamically as the slider moves
    const handleThresholdChange = (key, value) => {
        setThresholds((prev) => ({
          ...prev,
          [key]: value,
        }));
    };

    // Submit updated threshold to the backend
    const updateThreshold = async (country, instance, metric, threshold) => {
        try {
        const response = await fetch(`http://localhost:8088/alerts/set_threshold`, {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify({
            country,
            instance,
            metric,
            threshold: Number(threshold),
            }),
        });
    
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || "Failed to update threshold");
        }
    
        alert(`Threshold for ${metric} updated successfully!`);
        } catch (error) {
        console.error("Error updating threshold:", error);
        alert("Failed to update threshold.");
        }
    };
  

  
    return (
      <div className="min-h-screen bg-[#000230] text-white p-8">
        <h1 className="text-3xl font-bold mb-8">Alert Settings</h1>
  
        {/* App Selection */}
        <div className="mb-6">
          <label className="block text-lg mb-2">Select Application:</label>
          <select
            className="bg-gray-800 p-2 rounded-md w-full"
            onChange={(e) => handleAppChange(e.target.value)}
          >
            <option value="">-- Select an App --</option>
            {apps.map((app) => (
              <option key={app.app_id} value={app.app_id}>
                {app.app_name}
              </option>
            ))}
          </select>
        </div>
  
        {/* Country Selection */}
        <div className="mb-6">
          <label className="block text-lg mb-2">Select Country:</label>
          <select
            className="bg-gray-800 p-2 rounded-md w-full"
            onChange={(e) => setSelectedCountry(e.target.value)}
          >
            <option value="">-- Select a Country --</option>
            {Array.from(new Set(alerts.map((alert) => alert.country))).map(
              (country) => (
                <option key={country} value={country}>
                  {country}
                </option>
              )
            )}
          </select>
        </div>
  
        {/* Sliders */}
        {selectedApp && selectedCountry ? (
          <>
            {filteredAlerts.length > 0 ? (
              filteredAlerts.map((alert) => {
                const key = `${alert.instance_name}-${alert.metric}`;
                return (
                  <div key={key} className="mb-6">
                    <div className="flex justify-between mb-2">
                      <span>{alert.metric}</span>
                      <span>{thresholds[key] || alert.threshold}</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={thresholds[key] || alert.threshold}
                      onChange={(e) => handleThresholdChange(key, e.target.value)}
                      className="w-full"
                    />
                    <button
                      onClick={() =>
                        updateThreshold(
                          alert.country,
                          alert.instance_name,
                          alert.metric,
                          thresholds[key] || alert.threshold
                        )
                      }
                      className="mt-2 bg-blue-600 px-4 py-2 rounded-md"
                    >
                      Save
                    </button>
                  </div>
                );
              })
            ) : (
              <div>No alerts available for the selected app and country.</div>
            )}
          </>
        ) : (
          <div>Select both an application and a country to view alerts.</div>
        )}
      </div>
    );
  }
  
