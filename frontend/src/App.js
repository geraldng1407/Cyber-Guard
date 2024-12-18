import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import HomepageTime from './components/homepage/HomepageTime';
import HomepageSavedApps from './components/homepage/HomepageSavedApps';
import GlobalOverview from './components/homepage/GlobalOverview';
import ApplicationInstance from './components/applications/ApplicationInstance';
import ApplicationsMain from './components/applications/ApplicationsMain';
import ApplicationDetails from './components/applications/ApplicationDetails';
import CountriesMain from './components/countries/CountriesMain'
import CountryDetails from './components/countries/CountryDetails'
import AlertsHistory from './components/alerts/AlertsHistory';
import Settings from './components/Settings';

const App = () => {
  return (
    <Router>
      <div className="bg-[#000230] min-h-screen h-screen text-white flex flex-col">
        <NavBar />
        <div className="flex-grow">
          <Routes>
            <Route
              path="/"
              element={
                <div className="grid grid-cols-4 gap-6 p-6 h-full">
                  <div className="col-span-1 flex flex-col gap-6">
                    <HomepageTime />
                    <div className="border-b-2 border-gray-500" /> {/* This is the line */}
                    <HomepageSavedApps />
                  </div>
                  <div className="col-span-3 h-full flex flex-col">
                    <GlobalOverview />
                  </div>
                </div>
              }
            />
            <Route path="/applicationsmain" element={<ApplicationsMain />} />
            <Route path="/applications/:app_id" element={<ApplicationDetails />} />
            <Route path="/applicationsmain/A" element={<ApplicationDetails />} />
            <Route path="/instance/:instance_id" element={<ApplicationInstance />} />
            <Route path="/countriesmain" element={<CountriesMain />} />
            <Route path="/countries/:country" element={<CountryDetails />} />
            <Route path="/alerts/history" element={<AlertsHistory />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
