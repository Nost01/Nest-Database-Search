import { useState } from "react";

export default function Login({ onLogin }) {
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!password.trim()) return; // prevent empty submission
    onLogin(password);            // send password to App.js
    setPassword("");              // optional: clear field after submit
  };

  return (
    <div className="login-container">
      <h2>Enter Password</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
