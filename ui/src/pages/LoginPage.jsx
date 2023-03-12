import React, { useState } from "react";
import "../styles/login.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLoginSubmit = async (e) => {
    e.preventDefault();

    const apiUrl = "http://localhost/login/";

    // Get CSRF token from the server
    axios
      .get("http://localhost/csrf/", { withCredentials: true })
      .then((response) => {
        const csrfToken = response?.data?.csrfToken;

        if (csrfToken) {
          localStorage.setItem("csrfToken", true);

          // Set the CSRF token as a header on the Axios instance
          axios.defaults.headers.common["X-CSRFToken"] = csrfToken;
        }

        // Send the POST request with the login data and cookies
        const loginData = {
          username: login,
          password: password,
        };

        axios
          .post(apiUrl, loginData, { withCredentials: true })
          .then((response) => {
            if (response.status === 200) {
              navigate("/campaigns");
            }
          })
          .catch((err) => {
            console.error(err);
          });
      })
      .catch((error) => {
        console.error("ERROR", error);
      });
  };

  return (
    <div className="box">
      <form autoComplete="off" onSubmit={handleLoginSubmit}>
        <h2 className="signInText">Sign in</h2>
        <div className="inputBox">
          <input
            type="text"
            required="required"
            value={login}
            onChange={(e) => setLogin(e.target.value)}
          />
          <span>Username</span>
          <i></i>
        </div>
        <div className="inputBox">
          <input
            type="password"
            required="required"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <span>Password</span>
          <i></i>
        </div>
        <input className="loginSubmitInput" type="submit" value="Sign In" />
      </form>
    </div>
  );
};

export default LoginPage;
