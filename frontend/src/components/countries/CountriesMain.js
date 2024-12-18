import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import GlobalOverview from '../homepage/GlobalOverview';
import CountryDetails from './CountryDetails';

export default function CountriesMain() {
  return (
    <div className="h-screen bg-[#000230] text-white flex flex-col items-center">
      <div className="h-1/2 w-4/5">
        <GlobalOverview className="my-8" />
      </div>

      <section className="text-center mt-8 w-4/5">
        <h2 className="text-3xl font-semibold mb-6 text-center border-b border-gray-600 pb-4">
            Countries
          </h2>
        <div className="flex flex-wrap justify-center gap-6">
          <Dropdown label="ASIA-PACIFIC">
            <Link to="/countries/Singapore">
              <button className="bg-gray-700 px-6 py-3 rounded-md text-white w-full mb-3 transform transition-all duration-200 hover:bg-blue-600 hover:scale-105 hover:shadow-lg">
                Singapore
              </button>
            </Link>
            <Link to="/countries/China">
              <button className="bg-gray-700 px-6 py-3 rounded-md text-white w-full mb-3 transform transition-all duration-200 hover:bg-blue-600 hover:scale-105 hover:shadow-lg">
                China
              </button>
            </Link>
            <Link to="/countries/Japan">
              <button className="bg-gray-700 px-6 py-3 rounded-md text-white w-full mb-3 transform transition-all duration-200 hover:bg-blue-600 hover:scale-105 hover:shadow-lg">
                Japan
              </button>
            </Link>
          </Dropdown>

          <Dropdown label="EUROPE">
            <Link to="/countries/Germany">
              <button className="bg-gray-700 px-6 py-3 rounded-md text-white w-full mb-3 transform transition-all duration-200 hover:bg-blue-600 hover:scale-105 hover:shadow-lg">
                Germany
              </button>
            </Link>
          </Dropdown>

          <Dropdown label="LATIN AMERICA AND THE CARIBBEAN">
          </Dropdown>

          <Dropdown label="MIDDLE EAST AND AFRICA">
          </Dropdown>

          <Dropdown label="SWITZERLAND">
          </Dropdown>

          <Dropdown label="UNITED STATES AND CANADA">
            <Link to="/countries/UnitedStates">
              <button className="bg-gray-700 px-6 py-3 rounded-md text-white w-full mb-3 transform transition-all duration-200 hover:bg-blue-600 hover:scale-105 hover:shadow-lg">
                United States
              </button>
            </Link>
            <Link to="/countries/Canada">
              <button className="bg-gray-700 px-6 py-3 rounded-md text-white w-full mb-3 transform transition-all duration-200 hover:bg-blue-600 hover:scale-105 hover:shadow-lg">
                Canada
              </button>
            </Link>
          </Dropdown>
        </div>
      </section>

      <Routes>
        <Route path="/countries/:country" element={<CountryDetails />} />
      </Routes>
    </div>
  );
}

function Dropdown({ label, children }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="dropdown relative">
      <button
        className="bg-gray-700 px-6 py-3 rounded-md text-white w-full mb-4 transform transition-all duration-200 hover:bg-blue-600 hover:scale-105 hover:shadow-lg"
        onClick={() => setIsOpen(!isOpen)}
      >
        {label}
      </button>
      {isOpen && (
        <div className="dropdown-menu absolute bg-gray-800 mt-2 rounded-md p-4 space-y-2 shadow-lg transition-all duration-300 ease-in-out">
          {children}
        </div>
      )}
    </div>
  );
}
