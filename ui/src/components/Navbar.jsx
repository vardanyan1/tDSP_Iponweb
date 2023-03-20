import { useNavigate, useLocation, Link } from "react-router-dom";
import styles from "../styles/Navbar.module.css";
import Button from "./Button/Button";

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleClick = () => {
    localStorage.setItem("access", '');
    localStorage.setItem("refresh", '');
    navigate("/ui/");
  };

  const links = [
    { id: 1, to: "/ui/campaigns", text: "Campaigns" },
    { id: 2, to: "/ui/creatives", text: "Creatives" },
    { id: 3, to: "/ui/configure", text: "Configure" },
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
        <Button handleClick={handleClick} text="Logout" />
      </div>
    </div>
  );
};

export default Navbar;
