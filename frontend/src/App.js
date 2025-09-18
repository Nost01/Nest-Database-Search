import React, { useState } from 'react';
import Login from './components/login';
import SearchPage from './pages/SearchPage';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = async (password) => {
    try {
      const res = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ password }),
      });

      if (res.ok) {
        setIsAuthenticated(true);  
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
