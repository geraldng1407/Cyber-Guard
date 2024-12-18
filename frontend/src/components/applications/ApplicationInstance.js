import React, { useState, useEffect } from 'react';
import ApplicationInstanceMetricsTable from './ApplicationInstanceMetricsTable';
import ApplicationInstanceLogsTable from './ApplicationInstanceLogsTable';
import ApplicationInstanceSpansTable from './ApplicationInstanceSpansTable';
import MetricCharts from '../charts/MetricCharts';
import { useParams } from 'react-router-dom';

const ApplicationInstance = () => {
  const { instance_id } = useParams();
  const [logsExpanded, setLogsExpanded] = useState(false);
  const [spansExpanded, setSpansExpanded] = useState(false);
  const [metricsExpanded, setMetricsExpanded] = useState(false);
  const [instanceName, setInstanceName] = useState('Instance Name');
  const [activeAlerts, setActiveAlerts] = useState([]);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [alertToDelete, setAlertToDelete] = useState(null);

  useEffect(() => {
    const fetchInstanceName = async () => {
      try {
        const response = await fetch(`http://localhost:8088/instances/get_name/${instance_id}`);
        if (!response.ok) {
          throw new Error(`Error fetching instance name: ${response.statusText}`);
        }
        const data = await response.json();
        setInstanceName(data.instance_name.instance_name || 'Unknown Instance');
      } catch (error) {
        console.error('Failed to fetch instance name:', error);
        setInstanceName('Error fetching instance name');
      }
    };

    const fetchActiveAlerts = async () => {
      try {
        const response = await fetch(`http://localhost:8099/active_alerts`);
        if (!response.ok) {
          throw new Error(`Error fetching active alerts: ${response.statusText}`);
        }
        const data = await response.json();
        setActiveAlerts(data.filter(alert => alert.instance_id === instance_id));
      } catch (error) {
        console.error('Failed to fetch active alerts:', error);
      }
    };

    fetchInstanceName();
    fetchActiveAlerts();
  }, [instance_id]);

  const handleAlertClick = () => {
    setMetricsExpanded(true);
  };

  const handleDeleteAlert = async (id) => {
    try {
      const response = await fetch(`http://localhost:8099/active_alerts/${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error(`Error deleting alert: ${response.statusText}`);
      }
      const result = await response.json();
      console.log(result.message);
      setActiveAlerts((prevAlerts) => prevAlerts.filter((alert) => alert.id !== id));
    } catch (error) {
      console.error('Failed to delete alert:', error);
    } finally {
      setShowConfirmation(false);
      setAlertToDelete(null);
    }
  };

  const confirmDelete = (id) => {
    setAlertToDelete(id);
    setShowConfirmation(true);
  };

  const cancelDelete = () => {
    setAlertToDelete(null);
    setShowConfirmation(false);
  };

  return (
    <div className="flex flex-col h-screen bg-[#000230] text-white">
      <main className="flex-grow p-6">
        <div className="max-w-6xl mx-auto">
          <div className="mb-6">
            <h1 className="text-4xl font-bold">Instance Name: {instanceName}</h1>
            <p className="text-xl">Instance ID: {instance_id}</p>
          </div>

          <div className="flex gap-6">
            <div className="flex-grow flex flex-col gap-4 w-[60%]">
              {/* Active Alerts Section */}
              <div className="flex flex-col">
                <div className="flex justify-between items-center bg-red-700 px-4 py-2 rounded-md">
                  <span className="text-lg">ACTIVE ALERTS</span>
                </div>
                <div className="bg-red-700 rounded-md mt-2 overflow-hidden max-h-[30vh] overflow-y-auto">
                  {activeAlerts.length > 0 ? (
                    <table className="table-auto w-full text-left text-sm">
                      <thead>
                        <tr>
                          <th className="px-4 py-2">Metric</th>
                          <th className="px-4 py-2">Value</th>
                          <th className="px-4 py-2">Status</th>
                          <th className="px-4 py-2">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {activeAlerts.map((alert) => (
                          <tr key={alert.id} className="hover:bg-red-600">
                            <td className="px-4 py-2">{alert.metric}</td>
                            <td className="px-4 py-2">{alert.value}</td>
                            <td className="px-4 py-2">{alert.status}</td>
                            <td className="px-4 py-2">
                              <button
                                className="bg-gray-800 text-white px-2 py-1 rounded hover:bg-gray-600 mr-2"
                                onClick={handleAlertClick}
                              >
                                View Metrics
                              </button>
                              <button
                                className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-400"
                                onClick={() => confirmDelete(alert.id)}
                              >
                                Remove
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  ) : (
                    <p className="px-4 py-2">No active alerts for this instance.</p>
                  )}
                </div>
              </div>

              {/* Logs Section */}
              <div className="flex flex-col">
                <div
                  className="flex justify-between items-center cursor-pointer bg-gray-800 px-4 py-2 rounded-md"
                  onClick={() => setLogsExpanded(!logsExpanded)}
                >
                  <span className="text-lg">LOGS</span>
                  <span>{logsExpanded ? '▲' : '▼'}</span>
                </div>
                {logsExpanded && (
                  <div className="bg-gray-700 rounded-md mt-2 overflow-hidden max-h-[30vh] overflow-y-auto">
                    <ApplicationInstanceLogsTable logsExpanded={logsExpanded} instance_id={instance_id} />
                  </div>
                )}
              </div>

              {/* Spans Section */}
              <div className="flex flex-col">
                <div
                  className="flex justify-between items-center cursor-pointer bg-gray-800 px-4 py-2 rounded-md"
                  onClick={() => setSpansExpanded(!spansExpanded)}
                >
                  <span className="text-lg">SPANS</span>
                  <span>{spansExpanded ? '▲' : '▼'}</span>
                </div>
                {spansExpanded && (
                  <div className="bg-gray-700 rounded-md mt-2 overflow-hidden max-h-[30vh] overflow-y-auto">
                    <ApplicationInstanceSpansTable spansExpanded={spansExpanded} instance_id={instance_id} instanceName={instanceName} />
                  </div>
                )}
              </div>

              {/* Metrics Section */}
              <div className="flex flex-col">
                <div
                  className="flex justify-between items-center cursor-pointer bg-gray-800 px-4 py-2 rounded-md"
                  onClick={() => setMetricsExpanded(!metricsExpanded)}
                >
                  <span className="text-lg">METRICS</span>
                  <span>{metricsExpanded ? '▲' : '▼'}</span>
                </div>
                {metricsExpanded && (
                  <div className="bg-gray-700 rounded-md mt-2 overflow-hidden max-h-[50vh] overflow-y-auto">
                    <ApplicationInstanceMetricsTable metricsExpanded={metricsExpanded} instance_id={instance_id} instanceName={instanceName} />
                  </div>
                )}
              </div>
            </div>

            {/* Confirmation Popup */}
            {showConfirmation && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                <div className="bg-gray-800 text-white rounded-md p-6 w-96">
                  <h2 className="text-lg font-bold mb-4">Confirm Alert Removal</h2>
                  <p className="mb-6">Are you sure you want to remove this alert?</p>
                  <div className="flex justify-end gap-4">
                    <button
                      className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-400"
                      onClick={cancelDelete}
                    >
                      Cancel
                    </button>
                    <button
                      className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-400"
                      onClick={() => handleDeleteAlert(alertToDelete)}
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Metric Charts */}
            <div className="flex-shrink-0 w-[40%]">
              <div className="bg-gray-800 rounded-md h-[calc(100vh-10rem)] overflow-hidden">
                <div className="h-full overflow-y-auto p-4">
                  <MetricCharts instance_id={instance_id} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ApplicationInstance;