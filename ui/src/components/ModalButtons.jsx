import styles from "../styles/ModalButtons.module.css";

const ModalButtons = ({ handleToggleModal }) => {
  return (
    <div className={styles.buttonsWrapper}>
      <button id="save-btn" type="submit">
        Save
      </button>
      <button onClick={handleToggleModal} id="close-btn" type="button">
        Close
      </button>
    </div>
  );
};

export default ModalButtons;
