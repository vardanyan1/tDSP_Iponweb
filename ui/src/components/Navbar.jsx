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
    { id: 1, to: "/campaigns", text: "Campaigns" },
    { id: 2, to: "/creatives", text: "Creatives" },
    { id: 3, to: "/configure", text: "Configure" },
  ];

  const linkElements = links.map(({ id, to, text }) => (
    <Link
      key={id}
      to={to}
      className={location.pathname === to ? styles.active : ""}
    >
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
