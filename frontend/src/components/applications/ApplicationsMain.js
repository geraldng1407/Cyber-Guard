import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import ActiveAlerts from '../alerts/ActiveAlerts';

export default function ApplicationsMain() {
  const [allApplications, setAllApplications] = useState([]);
  const [categorizedApps, setCategorizedApps] = useState({});
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAllApplications = async () => {
      try {
        const response = await fetch('http://localhost:8088/applications');
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        setAllApplications(data);

        const categories = data.reduce((acc, app) => {
          if (!acc[app.app_type]) {
            acc[app.app_type] = [];
          }
          acc[app.app_type].push(app);
          return acc;
        }, {});

        setCategorizedApps({ All: data, ...categories });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAllApplications();
  }, []);

  if (loading) return <div className="text-center text-white">Loading...</div>;
  if (error) return <div className="text-center text-red-500">{error}</div>;

  return (
    <div className="h-screen bg-[#0D0D2B] text-white px-8 py-10">
      {/* Active Alerts Section */}
      <div className="flex flex-row h-1/2 mb-6">
        <section className="flex-1 bg-[#1A1A40] p-6 rounded-lg shadow-md h-full overflow-y-auto">
          <h2 className="text-3xl font-semibold mb-6 text-center border-b border-gray-600 pb-4">
            Active Alerts
          </h2>
          <div className="mt-4">
            <ActiveAlerts />
          </div>
        </section>
      </div>

      {/* Categorized Applications Section */}
      <div className="h-1/2 bg-[#1A1A40] p-6 rounded-lg shadow-md overflow-y-auto">
        <h2 className="text-3xl font-semibold mb-6 border-b border-gray-600 pb-4">
          All Applications
        </h2>

        {/* Category Dropdown */}
        <div className="mb-6">
          <label htmlFor="category-select" className="text-lg font-semibold mr-4">
            Select Category:
          </label>
          <select
            id="category-select"
            className="bg-[#2C2C58] text-white rounded-lg p-2 shadow-md focus:outline-none"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            {Object.keys(categorizedApps).map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>

        {/* Applications Display */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {categorizedApps[selectedCategory]?.map((app) => (
            <Link key={app.app_id} to={`/applications/${app.app_id}`}>
              <div className="flex flex-col items-center bg-[#2C2C58] p-6 rounded-lg hover:bg-[#3A3A66] transition-colors cursor-pointer shadow-md">
                <h4 className="text-lg font-semibold text-center">{app.app_name}</h4>
                <p className="text-sm text-gray-300 text-center mt-2">{app.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
