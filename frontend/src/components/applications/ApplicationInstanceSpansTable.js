import React, { useState, useEffect } from 'react';

// Helper function to fetch AppID from InstanceID
const fetchAppIdFromInstanceId = async (instanceId) => {
  try {
    const response = await fetch(`http://localhost:8088/instances/get_app_id/${instanceId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch app_id');
    }
    const jsonData = await response.json();
    return jsonData.app_id;
  } catch (error) {
    console.error('Error fetching app_id:', error);
    return null;
  }
};

// Fetch traces
const fetchTraces = async (appId) => {
  try {
    console.log('Fetching traces for App ID:', appId);
    const response = await fetch(`http://localhost:8088/traces/${appId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch spans');
    }

    const jsonData = await response.json();

    const traces = jsonData.traces || [];
    return traces.map((trace) => ({
      rootTraceName: trace.rootTraceName,
      rootServiceName: trace.rootServiceName,
      durationMs: trace.durationMs,
      spans: trace.spanSet.spans.map((span) => ({
        spanID: span.spanID,
        durationNanos: span.durationNanos,
        startTimeUnixNano: span.startTimeUnixNano,
        serviceName:
          span.attributes.find((attr) => attr.key === 'service.name')?.value.stringValue || 'Unknown',
      })),
    }));
  } catch (error) {
    console.error('Error fetching spans:', error);
    return [];
  }
};

const ApplicationInstanceSpansTable = ({ spansExpanded, instance_id, instanceName }) => {
  const [traces, setTraces] = useState(() => {
    const storedTraces = sessionStorage.getItem('traces');
    return storedTraces ? JSON.parse(storedTraces) : [];
  });

  const fetchTracesData = async () => {
    try {
      const appId = await fetchAppIdFromInstanceId(instance_id);
      if (!appId) {
        console.error('App ID could not be retrieved for the instance ID:', instance_id);
        return;
      }

      const traceData = await fetchTraces(appId);

      if (traceData.length > 0) {
        setTraces((prevTraces) => {
          const updatedTraces = [...prevTraces, ...traceData].slice(-20); // Keep only last 20 entries
          sessionStorage.setItem('traces', JSON.stringify(updatedTraces));
          return updatedTraces;
        });
      }
    } catch (error) {
      console.error('Error during spans fetch and processing:', error);
    }
  };

  useEffect(() => {
    if (spansExpanded) {
      fetchTracesData();
      const intervalId = setInterval(fetchTracesData, 5000);
      return () => clearInterval(intervalId); 
    }
  }, [spansExpanded, instance_id]);

  return (
    <div className="container mx-auto mt-8">
      {spansExpanded && (
        <div className="space-y-4">
          <div className="flex justify-between items-center bg-gray-800 p-4 rounded-t-lg">
            <h2 className="text-white text-lg font-semibold">Instance: {instanceName}</h2>
            {/* Refresh Button */}
            <button
              onClick={fetchTracesData}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded"
            >
              Refresh Spans
            </button>
          </div>
          <div className="relative overflow-y-auto h-96 border border-gray-700 rounded-b-lg">
            <table className="min-w-full table-fixed border-collapse">
              <thead className="sticky top-0 bg-gray-800 text-white">
                <tr>
                  <th className="w-1/4 px-4 py-2 border-b border-gray-700 text-left">Root Trace Name</th>
                  <th className="w-1/4 px-4 py-2 border-b border-gray-700 text-left">Service Name</th>
                  <th className="w-1/4 px-4 py-2 border-b border-gray-700 text-left">Duration (ms)</th>
                  <th className="w-1/4 px-4 py-2 border-b border-gray-700 text-left">Span ID</th>
                </tr>
              </thead>
              <tbody className="bg-gray-900 text-gray-300">
                {traces.map((trace, index) => (
                  trace.spans.map((span, idx) => (
                    <tr key={`${index}-${idx}`} className="hover:bg-gray-800">
                      <td className="px-4 py-2 border-b border-gray-700 break-words">
                        {trace.rootTraceName}
                      </td>
                      <td className="px-4 py-2 border-b border-gray-700 break-words">
                        {span.serviceName}
                      </td>
                      <td className="px-4 py-2 border-b border-gray-700 break-words">
                        {trace.durationMs}
                      </td>
                      <td className="px-4 py-2 border-b border-gray-700 break-words">
                        {span.spanID}
                      </td>
                    </tr>
                  ))
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default ApplicationInstanceSpansTable;
