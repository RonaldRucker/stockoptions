AppUI.jsx
// === React (frontend) ===
// File: src/App.jsx

import React, { useState } from 'react';
import './App.css';

function App() {
  const [ticker, setTicker] = useState('AAPL');
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchChart = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/chart?ticker=${ticker}`);
      const blob = await response.blob();
      setImageUrl(URL.createObjectURL(blob));
    } catch (error) {
      alert('Failed to fetch chart');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Stock Chart Viewer</h1>
      <input
        type="text"
        value={ticker}
        onChange={(e) => setTicker(e.target.value.toUpperCase())}
      />
      <button onClick={fetchChart}>Get Chart</button>
      {loading && <p>Loading...</p>}
      {imageUrl && <img src={imageUrl} alt="Stock Chart" style={{ width: '100%', maxWidth: 600 }} />}
    </div>
  );
}

export default App;
