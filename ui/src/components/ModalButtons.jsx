import styles from "../styles/ModalButtons.module.css";
import Button from "./Button/Button";

const ModalButtons = ({ handleToggleModal }) => {
  return (
    <div className={styles.buttonsWrapper}>
      <Button id="save-btn" type="submit" text="Save" />
      <Button
        id="close-btn"
        type="button"
        handleClick={handleToggleModal}
        text="Close"
      />
    </div>
  );
};

export default ModalButtons;
