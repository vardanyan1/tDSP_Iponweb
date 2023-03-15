import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../axios-instance";
import styles from "../styles/Login.module.css";

const LoginPage = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLoginSubmit = async (e) => {
    e.preventDefault();

    try {
      // Get CSRF token from the server
      const response = await axios.get("/csrf/", {
        withCredentials: true,
      });
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

      const loginResponse = await axios.post("/login/", loginData, {
        withCredentials: true,
      });
      if (loginResponse.status === 200) {
        navigate("/campaigns");
      }
    } catch (error) {
      console.error("ERROR", error);
    }
  };

  return (
    <div className={styles.box}>
      <form
        className={styles.loginForm}
        autoComplete="off"
        onSubmit={handleLoginSubmit}
      >
        <h2 className={styles.signInText}>Sign in</h2>
        <div className={styles.inputBox}>
          <input
            type="text"
            required
            value={login}
            onChange={(e) => setLogin(e.target.value)}
          />
          <span>Username</span>
          <i></i>
        </div>
        <div className={styles.inputBox}>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <span>Password</span>
          <i></i>
        </div>
        <input
          className={styles.loginSubmitInput}
          type="submit"
          value="Sign In"
        />
      </form>
    </div>
  );
};

export default LoginPage;
