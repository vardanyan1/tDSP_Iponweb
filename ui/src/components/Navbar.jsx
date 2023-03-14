import { useNavigate } from "react-router-dom";
import PageNavigations from './PageNavigations';
import Logout from './Logout';
import styles from '../styles/Navbar.module.css';

const Navbar = () => {
  return (
    <div className={styles.navbarWrapper}>
        <PageNavigations />
        <Logout />
    </div>
  );
};

export default Navbar;
