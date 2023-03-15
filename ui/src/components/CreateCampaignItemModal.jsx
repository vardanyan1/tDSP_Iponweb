import React, { useEffect, useState } from "react";
import styles from "../styles/CampaignItemModal.module.css";

const CreateCampaignItemModal = ({
  handleToggleModal,
  modalRef,
  handleCreateCampaignItem,
}) => {
  const [newItem, setNewItem] = useState({
    name: "",
    budget: "",
  });
  const [errorType, setErrorType] = useState({
    name: false,
    budget: false,
  });

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (event.target.id === "overlay") {
        handleToggleModal();
      }
    };

    document.addEventListener("click", handleOutsideClick);

    return () => {
      document.removeEventListener("click", handleOutsideClick);
    };
  }, [handleToggleModal]);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    if (name === "budget") {
      const regex = /^[0-9]+$/;
      const isNumber = regex.test(value);
      if (!isNumber) return;
    }
    setNewItem((prevState) => ({
      ...prevState,
      [name]: value,
    }));
    setErrorType((prevState) => ({
      ...prevState,
      [name]: !value,
    }));
  };

  const handleBlur = (event) => {
    const { name, value } = event.target;
    setErrorType((prevState) => ({
      ...prevState,
      [name]: !value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const { name, budget } = newItem;
    if (!name || !budget) {
      setErrorType({
        name: !name,
        budget: !budget,
      });
      return;
    }
    handleCreateCampaignItem(newItem);
  };

  return (
    <div>
      <div id="modal" className={styles.modal} ref={modalRef}>
        <div className={styles.modalContent}>
          <form onSubmit={handleSubmit} className={styles.createCampaignsModal}>
            <div className={styles.inputsWrapper}>
              <input
                type="text"
                id="name"
                name="name"
                placeholder="Campaign name"
                value={newItem.name}
                style={{
                  borderColor: errorType.name ? "red" : undefined,
                }}
                onBlur={handleBlur}
                onChange={handleInputChange}
              />
              <input
                type="text"
                id="budget"
                name="budget"
                placeholder="Budget"
                value={newItem.budget}
                style={{
                  borderColor: errorType.budget ? "red" : undefined,
                }}
                onBlur={handleBlur}
                onChange={handleInputChange}
              />
            </div>
            <div className={styles.campaignModalBtnWrapper}>
              <button
                className={styles.saveCampaignItem}
                id="save-btn"
                type="submit"
              >
                Save
              </button>
              <button
                className={styles.closeCampaignItemModal}
                onClick={handleToggleModal}
                id="close-btn"
                type="button"
              >
                Close
              </button>
            </div>
          </form>
        </div>
      </div>
      <div id="overlay" className={styles.overlay}></div>
    </div>
  );
};

export default CreateCampaignItemModal;
