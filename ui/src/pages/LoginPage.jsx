import React, { useState } from "react";
import "../styles/LoginStyles.css";
import axios from "axios"

const LoginPage = () => {
  const [login, setLogin] = useState('');
  const [pass, setPass] = useState('');

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    const apiUrl = 'http://localhost:8000/login/';

    // Get CSRF token from the server
      axios.get('http://localhost:8000/csrf/', { withCredentials: true })
        .then(response => {
            const csrfToken = response.data.csrfToken;

      // Set the CSRF token as a header on the Axios instance
      axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

      // Send the POST request with the login data and cookies
      const loginData = {
          username: login,
          password: pass
      };
      axios.post(apiUrl, loginData, { withCredentials: true })
        .then(response => {
            if(response.status === 200) {
                window.location.href = 'http://localhost:3000/campaigns/';
            }
        })
        .catch(err => {
            console.error(err)
        })
       })
    .catch(error => {
      console.error('ERROR', error);
    })
  };

  return (
    <div className="formWrapper">
      <form className="loginForm">
        <input
          type="text"
          placeholder="Login"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={pass}
          onChange={(e) => setPass(e.target.value)}
        />
        <button onClick={handleLoginSubmit}>Sign In</button>
      </form>
    </div>
  );
};

export default LoginPage;
