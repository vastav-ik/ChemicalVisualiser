import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
    }
  }, [token]);

  return (
    <div className="App">
      {!token ? (
        <Login setToken={setToken} />
      ) : (
        <Dashboard token={token} setToken={setToken} />
      )}
    </div>
  );
}

export default App;
