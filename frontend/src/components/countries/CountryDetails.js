import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Pie } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

export default function CountryDetails() {
    const { country } = useParams(); // Get the country from URL parameters
    const [instancesData, setInstancesData] = useState([]);
    const [issuesData, setIssuesData] = useState([]);
    const [pastIssuesData, setPastIssuesData] = useState([]); // For past issues
    const [filteredPastIssues, setFilteredPastIssues] = useState([]); // For filtered past issues
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [appFilter, setAppFilter] = useState('');
    const [metricFilter, setMetricFilter] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Fetch instances for country
                const instancesResponse = await fetch(`http://localhost:8088/instances/${country}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (!instancesResponse.ok) {
                    throw new Error('Failed to fetch instances data');
                }
                const instancesResult = await instancesResponse.json();
                setInstancesData(instancesResult);

                // Fetch active issues
                const issuesResponse = await fetch(`http://localhost:8099/active_alerts`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (!issuesResponse.ok) {
                    throw new Error('Failed to fetch issues data');
                }
                const issuesResult = await issuesResponse.json();
                console.log('issuesResult:', issuesResult);

                if (Array.isArray(issuesResult)) {
                    const countryIssues = issuesResult.filter(issue => issue.country === country);
                    setIssuesData(countryIssues);
                } else if (issuesResult.message === "No active alerts") {
                    console.warn(issuesResult.message); 
                    setIssuesData([]); 
                } else {
                    console.error('Unexpected issues data format:', issuesResult);
                    setIssuesData([]); 
                }

                // Fetch past issues
                const pastIssuesResponse = await fetch(`http://localhost:8099/alerts_logs/all`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (!pastIssuesResponse.ok) {
                    throw new Error('Failed to fetch past issues data');
                }
                const pastIssuesResult = await pastIssuesResponse.json();
                
                const countryPastIssues = pastIssuesResult.filter(issue => issue.country === country);
                setPastIssuesData(countryPastIssues);
                setFilteredPastIssues(countryPastIssues);

            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [country]);

    useEffect(() => {
        const filtered = pastIssuesData.filter(issue => {
            const appMatches = appFilter ? issue.app_name === appFilter : true;
            const metricMatches = metricFilter ? issue.metric === metricFilter : true;
            return appMatches && metricMatches;
        });
        setFilteredPastIssues(filtered);
    }, [appFilter, metricFilter, pastIssuesData]);

    const clearFilters = () => {
        setAppFilter('');
        setMetricFilter('');
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    const unhealthyCount = issuesData.length;
    const healthyCount = instancesData.length - unhealthyCount;

    const chartData = {
        labels: ['Healthy Instances', 'Unhealthy Instances'],
        datasets: [
            {
                data: [healthyCount, unhealthyCount],
                backgroundColor: ['#4CAF50', '#F44336'],
                hoverBackgroundColor: ['#66BB6A', '#E57373'],
            },
        ],
    };

    const appNames = [...new Set(pastIssuesData.map(issue => issue.app_name))];
    const metrics = [...new Set(pastIssuesData.map(issue => issue.metric))];

    return (
        <div className="min-h-screen bg-[#0D0D2B] text-white p-8">
            <div className="grid grid-cols-3 gap-8">
                <section className="col-span-1 bg-gray-800 p-6 rounded-lg shadow-md">
                    <h2 className="text-2xl font-semibold mb-4">Overall Health</h2>
                    <div className="bg-[#000230] h-3/4 flex items-center justify-center">
                        <Pie data={chartData} />
                    </div>
                </section>

                <section className="col-span-2">
                    <h2 className="text-3xl font-semibold mb-4">{country}</h2>
                    <div className="mb-8 overflow-y-auto">
                        <h3 className="text-xl font-semibold mb-4">Instances Used</h3>
                        <div className="flex flex-wrap gap-4">
                            {instancesData.map((item, index) => {
                                const isUnhealthy = issuesData.some(issue => String(issue.instance_id) === String(item.instance_id));

                                return (
                                    <a
                                        key={index}
                                        href={`http://localhost:3001/instance/${item.instance_id}`}
                                        className="flex flex-col items-center text-center w-24"
                                    >
                                        <div
                                            className={`w-16 h-16 rounded-full flex items-center justify-center ${
                                                isUnhealthy ? 'bg-red-500' : 'bg-green-500'
                                            }`}
                                        >
                                            <span className="text-3xl">
                                                {isUnhealthy ? '⚠️' : '📂'}
                                            </span>
                                        </div>
                                        <span className="text-sm mt-2">
                                            {item.app_name}-{item.instance_id}
                                        </span>
                                    </a>
                                );
                            })}
                        </div>
                    </div>

                    <div className="mb-8">
                        <h3 className="text-xl font-semibold mb-4">Active Issues</h3>
                        <div className="space-y-4">
                            {issuesData.length > 0 ? (
                                issuesData.map((issue, index) => (
                                    <div
                                        key={index}
                                        className="flex items-center justify-between bg-gray-700 p-4 rounded-lg cursor-pointer"
                                        onClick={() => window.location.href = `http://localhost:3001/instance/${issue.instance_id}`}
                                    >
                                        <div className="flex items-center">
                                            <span className="material-icons text-red-500 text-4xl mr-4">⚠️</span> 
                                            <div>
                                                <p className="font-bold">{issue.instance}</p>
                                                <p className="text-red-500">{issue.metric}</p>
                                                <p className="text-sm">Logged at: {issue.logged_at}</p>
                                            </div>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="flex items-center justify-center bg-gray-700 p-4 rounded-lg">
                                    <span className="material-icons text-red-500 text-4xl mr-4">⚠️</span> 
                                    <p className="text-center text-red-500 font-bold">No Active Issues for {country}</p>
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="mb-8">
                        <h3 className="text-xl font-semibold mb-4">Past Issues</h3>
                        
                        {/* Filter Dropdowns and Clear Filters Button */}
                        <div className="flex gap-4 mb-4 items-center">
                            {/* Application Filter Dropdown */}
                            <div className="flex items-center">
                                <label className="mr-2">Application:</label>
                                <select
                                    className="p-2 rounded bg-gray-800 text-white"
                                    value={appFilter}
                                    onChange={(e) => setAppFilter(e.target.value)}
                                >
                                    <option value="">Select Application</option>
                                    {appNames.map((appName, index) => (
                                        <option key={index} value={appName}>
                                            {appName}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            {/* Metric Filter Dropdown */}
                            <div className="flex items-center">
                                <label className="mr-2">Metric:</label>
                                <select
                                    className="p-2 rounded bg-gray-800 text-white"
                                    value={metricFilter}
                                    onChange={(e) => setMetricFilter(e.target.value)}
                                >
                                    <option value="">Select Metric</option>
                                    {metrics.map((metric, index) => (
                                        <option key={index} value={metric}>
                                            {metric}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            {/* Clear Filters Button */}
                            <button 
                                onClick={clearFilters}
                                className="px-4 py-2 bg-red-500 text-white rounded-lg"
                            >
                                Clear Filters
                            </button>
                        </div>

                        <div className="max-h-80 overflow-y-auto">
                            <table className="min-w-full text-left">
                                <thead className="bg-[#000230]">
                                    <tr>
                                        <th className="px-6 py-2">Application</th>
                                        <th className="px-6 py-2">Metric</th>
                                        <th className="px-6 py-2">Value</th>
                                        <th className="px-6 py-2">Logged At</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-[#000230]">
                                    {filteredPastIssues.length > 0 ? (
                                        filteredPastIssues.map((issue, index) => (
                                            <tr key={index} className="border-t border-gray-700 hover:bg-[#001F3F]">
                                                <td className="px-6 py-4">{issue.app_name}</td>
                                                <td className="px-6 py-4">{issue.metric}</td>
                                                <td className="px-6 py-4">{issue.value}</td>
                                                <td className="px-6 py-4">{issue.logged_at}</td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr>
                                            <td colSpan="4" className="px-6 py-4 text-center text-red-500">
                                                No past issues found for the selected filters.
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    );
}