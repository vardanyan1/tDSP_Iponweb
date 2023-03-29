import { useState } from "react";
import { useLogin } from "../hooks/useLogin";
import styles from "../styles/Login.module.css";

const LoginPage = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const { handleLogin, error, isLoading } = useLogin();

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

    handleLogin(loginData);
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
          disabled={isLoading}
        />
      </form>
    </div>
  );
};

export default LoginPage;
