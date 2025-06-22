import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';

function App() {
  const [selection, setSelection] = useState('Option 1');
  const [ticker, setTicker] = useState('');
  const [lastPrice, setLastPrice] = useState(null);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (event) => {
    setSelection(event.target.value);
  };

  const handleTickerChange = (event) => {
    setTicker(event.target.value.toUpperCase());
  };

  const handleSearch = async (event) => {
    event.preventDefault();
    setSearching(true);
    setError('');
    setLastPrice(null);
    try {
      const response = await fetch(`http://localhost:8000/price?ticker=${ticker}`);
      if (!response.ok) {
        throw new Error('Ticker not found or server error');
      }
      const data = await response.json();
      setLastPrice(data.price);
    } catch (err) {
      setError(err.message);
    }
    setSearching(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <div>
          <label htmlFor="dropdown" style={{ marginRight: '8px' }}>Choose an option:</label>
          <select id="dropdown" value={selection} onChange={handleChange}>
            <option value="Option 1">Option 1</option>
            <option value="Option 2">Option 2</option>
          </select>
        </div>
        <form onSubmit={handleSearch} style={{ marginTop: '24px' }}>
          <label htmlFor="ticker" style={{ marginRight: '8px' }}>Search Ticker:</label>
          <input
            id="ticker"
            type="text"
            value={ticker}
            onChange={handleTickerChange}
            placeholder="e.g. AAPL"
            style={{ marginRight: '8px' }}
          />
          <button type="submit" disabled={!ticker || searching}>
            {searching ? 'Searching...' : 'Search'}
          </button>
        </form>
        {lastPrice !== null && (
          <p style={{ marginTop: '16px' }}>
            Last price for <b>{ticker}</b>: {lastPrice}
          </p>
        )}
        {error && (
          <p style={{ color: 'red', marginTop: '16px' }}>{error}</p>
        )}
        <p style={{ marginTop: '16px' }}>You selected: {selection}</p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
