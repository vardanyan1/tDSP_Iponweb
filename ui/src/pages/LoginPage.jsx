import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "react-query";
import axios from "../axios-instance";
import styles from "../styles/Login.module.css";

const LoginPage = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);
  const navigate = useNavigate();

  const loginMutation = useMutation(
    (loginData) => axios.post("/api/token/", loginData),
    {
      onSuccess: (data) => {
        localStorage.setItem("token", data.data.access);
        localStorage.setItem("refresh", data.data.refresh);
        navigate("/ui/campaigns");
      },
      onError: (error) => {
        console.error("ERROR", error);
        setError(true);
      },
    }
  );

  const handleLoginInputChange = (e) => {
    const { name, value } = e.target;
    if (name === "login") {
      setLogin(value);
    } else if (name === "password") {
      setPassword(value);
    }
  };

  const handleLoginSubmit = (e) => {
    e.preventDefault();

    const loginData = {
      username: login,
      password: password,
    };

    loginMutation.mutate(loginData);
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
            name="login"
            required
            value={login}
            onChange={handleLoginInputChange}
          />
          <span>Username</span>
          <i></i>
        </div>
        <div className={styles.inputBox}>
          <input
            type="password"
            name="password"
            required
            value={password}
            onChange={handleLoginInputChange}
          />
          <span>Password</span>
          <i></i>
        </div>
        {error && (
          <p className={styles.error}>
            Please, enter a valid Username or Password
          </p>
        )}
        <input
          className={styles.loginSubmitInput}
          type="submit"
          value="Sign In"
          disabled={loginMutation.isLoading}
        />
      </form>
    </div>
  );
};

export default LoginPage;
