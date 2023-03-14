import { useNavigate } from "react-router-dom";
import styles from '../styles/Logout.module.css';

const Logout = () => {
  const navigate = useNavigate();

    const handleClick = () => {
        localStorage.setItem('csrfToken', false);
        navigate('./login')
    }

  return (
    <div className={styles.logoutWrapper}>
      <button onClick={handleClick}>Logout</button>
    </div>
  );
};

export default Logout;
