import React, { useState, useEffect } from 'react';
import NavBar from './components/NavBar';
import HomepageTime from './components/HomepageTime';
import HomepageSavedApps from './components/HomepageSavedApps';
import GlobalOverview from './components/GlobalOverview';
import ActiveAlerts from './components/alerts/ActiveAlerts';

const Homepage = () => {
  return (
    <div className="bg-[#000230] min-h-screen text-white">
      <NavBar />
      <div className="grid grid-cols-4 gap-4 p-4">
        <div className="col-span-1 flex flex-col">
          <div className="mb-6">
            <HomepageTime />
          </div>
          <div className="flex-1 bg-gray-800 rounded-lg p-4 overflow-y-auto">
            <HomepageSavedApps />
          </div>
        </div>

        <div className="col-span-3">
          <div className="px-20 pb-4">
            <GlobalOverview />
          </div>
          <div className="p-4">
            <ActiveAlerts />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Homepage;
