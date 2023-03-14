import React, { useEffect, useState } from "react";
import styles from "../styles/CampaignItemModal.module.css";

const CreateCampaignItemModal = ({
  handleToggleModal,
  modalRef,
  handleCreateCampaignItem,
}) => {
  const [newItem, setNewItem] = useState({
    name: undefined,
    budget: undefined,
    isDisabled: true,
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

  const handleInputChange = (type) => (e) => {
    if (type === "budget") {
      const regex = /^[0-9]+$/;
      const isNumber = regex.test(e.target.value);
      if (!isNumber) return;
    }
    setErrorType((prevState) => ({
      ...prevState,
      [type]: !e.target.value,
    }));
    setNewItem((prevState) => ({
      ...prevState,
      [type]: e.target.value,
    }));
  };

  const handleBlur = (type) => (e) => {
    setErrorType((prevState) => ({
      ...prevState,
      [type]: !e.target.value,
    }));
  };

  const handleSubmit = (formValues) => (event) => {
    event.preventDefault();
    if (!formValues.name || !formValues.budget) {
      setErrorType((prevState) => ({
        ...prevState,
        name: !formValues.name,
        budget: !formValues.budget,
      }));
      return;
    }
    handleCreateCampaignItem(formValues);
  };

  console.log({ errorType });

  return (
    <div>
      <div id="modal" className={styles.modal} ref={modalRef}>
        <div className={styles.modalContent}>
          <form
            onSubmit={handleSubmit(newItem)}
            className={styles.createCampaignsModal}
          >
            <div className={styles.inputsWrapper}>
              <input
                type="text"
                id="name"
                name="name"
                placeholder="Campaign name"
                value={newItem.name || ""}
                style={{
                  borderColor: errorType?.name ? "red" : undefined,
                }}
                onBlur={handleBlur("name")}
                onChange={handleInputChange("name")}
              />
              <input
                type="text"
                id="budget"
                name="budget"
                placeholder="Budget"
                value={newItem.budget || ""}
                style={{
                  borderColor: errorType?.budget ? "red" : undefined,
                }}
                onBlur={handleBlur("budget")}
                onChange={handleInputChange("budget")}
              />
              {/* <input
                type="text"
                id="bidFloor"
                name="bid floor"
                placeholder="Bid floor"
                value={bidFloorValue}
                onChange={handleInputChange}
              /> */}
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
