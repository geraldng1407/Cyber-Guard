import React, { useState, useEffect, useMemo } from 'react';
import { useParams } from "react-router-dom";
import { FunnelIcon } from '@heroicons/react/24/outline';

const fetchLogs = async (url) => {
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch logs');
    }

    const jsonData = await response.json();
  
    return jsonData || [];  
  } catch (error) {
    console.error('Error fetching logs:', error);
    return []; 
  }
};

const rearrangeLogKeys = (log) => {
  return {
    Timestamp: log.logged_at,  
    Country: log.code,
    Instance: log.instance,
    App: log.app_name,
    Metric: log.metric,
    Value: log.value,
    Status: log.status
  };
};

const AlertsHistoryTable = () => {
  const [logs, setLogs] = useState(() => {
    const storedLogs = sessionStorage.getItem('logs');
    return storedLogs ? JSON.parse(storedLogs) : [];
  });

  useEffect(() => {
    const fetchAndSetLogs = async () => {
      const url = 'http://localhost:8099/alerts_logs/all'; 
      const logData = await fetchLogs(url);
      const reorderedLogs = logData.map(rearrangeLogKeys);
      setLogs(reorderedLogs);
    };

    fetchAndSetLogs();
  }, []);

  // const headers = Object.keys(logs[0]);
  const headers = logs.length > 0 ? Object.keys(logs[0]) : [];

  const filterableHeaders = ['Status', 'Metric', 'App', 'Instance', 'Country'];

  const [filters, setFilters] = useState(
    filterableHeaders.reduce((acc, header) => ({ ...acc, [header]: [] }), {})
  );

  const [dropdownOpen, setDropdownOpen] = useState(null);

  const handleDropdownToggle = (header) => {
    setDropdownOpen((prev) => (prev === header ? null : header));
  };

  useEffect(() => {
    const savedFilters = JSON.parse(localStorage.getItem('filters'));
    if (savedFilters) {
      setFilters(savedFilters);
    }
  }, []);

  useEffect(() => {
    if (filters) {
      localStorage.setItem('filters', JSON.stringify(filters));
    }
  }, [filters]);

  const columnValues = useMemo(() => {
    const values = {};
    headers.forEach((header) => {
      values[header] = ['All', ...new Set(logs.map((log) => log[header]))];
    });
    return values;
  }, [logs, headers]);

  const handleFilterChange = (header, value) => {
    setFilters((prevFilters) => {

      if (value === 'All') {
        return { ...prevFilters, [header]: [] };
      }
  
      return {
        ...prevFilters,
        [header]: prevFilters[header].includes(value)
          ? prevFilters[header]
          : [...prevFilters[header], value],
      };
    });
    setDropdownOpen(null); 
  };

  const filteredLogs = logs.filter((log) => {
    return Object.keys(filters).every((header) => {
      if (filters[header].length === 0) return true;
  
      return filters[header].includes(log[header]);
    });
  });

  const removeFilter = (header, value) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      [header]: prevFilters[header].filter((filterValue) => filterValue !== value),
    }));
  };
  
  const clearAllFilters = () => {
    setFilters(
      filterableHeaders.reduce((acc, header) => ({ ...acc, [header]: [] }), {})
    );
  };

  return (
    <div className="container mx-auto h-full w-full">
      {(
      <div className="space-y-4 h-full">
      {/* Display currently applied filters */}
      <div className="mb-4">
      <span className="ml-4 font-bold">Applied Filters:</span>
          {Object.entries(filters).every(([header, values]) => values.length === 0) ? (
            <span className="ml-4">No filters applied</span>
          ) : (
            <div className="flex flex-wrap inline-flex">
              {Object.entries(filters).map(([header, values]) =>
                values.length > 0 ? (
                  <div key={header} className="mr-6 inline-flex items-center">
                    <span className="ml-4 font-bold">{header}:</span>
                    <div className="flex flex-wrap">
                      {values.map((value, idx) => (
                        <span
                          key={idx}
                          className="mr-2 inline-flex items-center bg-gray-700 text-white py-1 px-3 rounded-full text-sm"
                        >
                          {value}{' '}
                          <button
                            onClick={() => removeFilter(header, value)}
                            className="ml-2 text-red-500"
                          >
                            &times; 
                          </button>
                        </span>
                      ))}
                    </div>
                  </div>
                ) : null
              )}
            </div>
          )}
          {/* Button to clear all filters */}
          {Object.entries(filters).some(([header, values]) => values.length > 0) && (
            <button
              onClick={clearAllFilters}
              className="ml-4 text-blue-500"
            >
              Clear All Filters
            </button>
          )}
        </div>

          <div className="relative overflow-y-auto h-full border border-gray-700 rounded-b-lg">
            <table className="min-w-full table-fixed border-collapse" >
              <thead className="sticky top-0 bg-gray-800 text-white">
              <tr>
                {headers.map((header) => (
                  <th key={header} className="px-4 py-2 border-b text-left">
                    <div className="flex items-center justify-between"> {/* Align header content */}
                      {header}
                      {/* Filter Button with Dropdown */}
                      {filterableHeaders.includes(header) && (
                        <button
                          className="ml-2 text-gray-500"
                          onClick={() => handleDropdownToggle(header)}>
                          <FunnelIcon className="h-5 w-5 fill-current" />
                        </button>
                      )}
                    </div>
                    {dropdownOpen === header && (
                      <div className="absolute bg-white shadow-lg rounded-md mt-2 w-40 text-black">
                        <ul className="py-2"> 
                            {columnValues[header]?.map((value, idx) => (
                            <li
                              key={idx}
                              className="px-4 py-2 hover:bg-gray-200 cursor-pointer"
                              onClick={() => handleFilterChange(header, value)}
                            >
                              {value}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </th>
                ))}
              </tr>
              </thead>
                <tbody>
                  {filteredLogs.map((log, index) => (
                    <tr key={index}>
                      {headers.map((header) => (
                        <td key={header} className="px-4 py-2 border-b truncated">
                          {header === 'Status' ? (
                            <span
                              className={
                                log[header] === 'Red' ? 'text-red-500' : log[header] === 'Green' ? 'text-green-500' : ''
                              }
                            >
                              {log[header]}
                            </span>
                          ) : (
                            log[header]
                          )}
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

const AlertsHistory = () => {

  return (
    <div className="flex flex-col h-screen bg-[#000230] text-white">
      <main className="flex-grow p-6">
        <div className="max-w-6xl mx-auto h-screen">
          <div className="mb-6">
            <h1 className="text-4xl font-bold">Alerts History</h1>
          </div>
          <div className="flex gap-6 h-[80vh]">
            <div className="flex-grow">
              <div className="bg-gray-700 rounded-md mt-2 h-[70vh] overflow-hidden">
                  <AlertsHistoryTable />
              </div>
            </div>
            
          </div>
        </div>
      </main>
    </div>
  );
};

export default AlertsHistory;