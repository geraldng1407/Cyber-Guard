import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

export default function HomepageSavedApps() {
  const [applications, setApplications] = useState([]);
  
  useEffect(() => {
    async function fetchSavedApplications() {
      try {
        const response = await fetch('http://localhost:8088/saved/app');
        const data = await response.json();
        setApplications(data);
      } catch (error) {
        console.error("Error fetching saved applications:", error);
      }
    }

    fetchSavedApplications();
  }, []);

  return (
    <div>
      <h3 className="text-2xl font-bold mb-6 text-white">Saved Applications</h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
        {applications.map((app) => (
          <Link
            key={app.app_id}
            to={`/applications/${app.app_id}`}
            className="bg-[#1E293B] p-6 rounded-lg text-center flex flex-col items-center justify-center transition-transform transform hover:scale-105 hover:bg-[#374151] shadow-lg"
          >
            <div className="text-3xl mb-2">📂</div>
            <div className="text-sm text-white font-medium">{app.app_name}</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
