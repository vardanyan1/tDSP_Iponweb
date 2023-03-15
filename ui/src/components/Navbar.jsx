import { useNavigate, useLocation, Link } from "react-router-dom";
import styles from "../styles/Navbar.module.css";

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleClick = () => {
    localStorage.setItem("csrfToken", false);
    navigate("/");
  };

  const links = [
    { to: "/campaigns", text: "Campaigns" },
    { to: "/creatives", text: "Creatives" },
    { to: "/configure", text: "Configure" },
  ];

  const linkElements = links.map(({ to, text }) => (
    <Link to={to} className={location.pathname === to && styles.active}>
      {text}
    </Link>
  ));

  return (
    <div className={styles.navbarWrapper}>
      <div></div>
      <div className={styles.navigationLinksWrapper}>{linkElements}</div>
      <div className={styles.logoutWrapper}>
        <button onClick={handleClick}>Logout</button>
      </div>
    </div>
  );
};

export default Navbar;
