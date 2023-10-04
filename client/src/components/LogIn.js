import React, { useState } from "react";
import { Link } from "react-router-dom";
import DogHouseDetails from "./DogHouseDetails";

function LogIn({ user, setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    }).then((r) => {
      if (r.ok) {
        console.log(r)
        r.json().then((user) => setUser(user));
      }
    });
  }

  return (
    <div>
      {user ? (
        <DogHouseDetails />
      ) : (
        <div>
        <form onSubmit={handleSubmit}>
        <h1>Login</h1>
        <label htmlFor="email">Email</label>
        <input
          type="text"
          id="email"
          autoComplete="off"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        /><br></br>
        
        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        /><br></br>
        <button type="submit">Login</button>
      </form>
      

      <Link to={`/signUp`}>Don't have an account? Register</Link>
      </div>
      )}
      
    </div>
  );
}

export default LogIn;
