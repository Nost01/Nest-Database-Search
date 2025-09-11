import React, { useState } from 'react';
import Login from './components/login';
import SearchPage from './pages/SearchPage';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const API_URL = process.env.REACT_APP_API_URL;

  const handleLogin = async (password) => {
    try {
      const res = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ password }),
      });

      if (res.ok) {
        setIsAuthenticated(true);   // ✅ only set true if password is correct
      } else {
        alert("Invalid password, please try again.");
      }
    } catch (err) {
      alert("Login failed, please try again.");
      console.error(err);
    }
  }

  return (
    <>
      {!isAuthenticated ? (
        <Login onLogin={handleLogin} />
      ) : (
        <SearchPage />
      )}
    </>
  );
}
