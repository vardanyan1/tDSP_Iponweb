import styles from "./Header.module.css";

const Header = ({ text }) => {
  return (
    <div className={styles.row}>
      <div className={styles.headerWrapper}>
        <h2>{text}</h2>
      </div>
    </div>
  );
};

export default Header;
