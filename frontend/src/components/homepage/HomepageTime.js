import React, { useState, useEffect } from 'react';

export default function HomepageTime() {
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date().toLocaleTimeString());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="text-center text-white">
      <h2 className="text-4xl">Local Time</h2>
      <p className="text-6xl font-bold">{time}</p>
    </div>
  );
}