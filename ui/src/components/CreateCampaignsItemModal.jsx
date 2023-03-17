import React, { useEffect, useState } from "react";
import styles from "../styles/CampaignsItemModal.module.css";
import Input from "./Input";
import ModalButtons from "./ModalButtons";

const CreateCampaignsItemModal = React.memo(
  ({ handleToggleModal, handleCreateCampaignsItem }) => {
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
      if (name === "budget" && value.length) {
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
      handleCreateCampaignsItem(newItem);
    };

    return (
      <div>
        <div id="modal" className={styles.modal}>
          <div className={styles.modalContent}>
            <form
              onSubmit={handleSubmit}
              className={styles.createCampaignsModal}
            >
              <div className={styles.inputsWrapper}>
                <Input
                  type="text"
                  id="name"
                  name="name"
                  placeholder="Campaign name"
                  value={newItem.name}
                  error={errorType.name}
                  onBlur={handleBlur}
                  onChange={handleInputChange}
                />
                <Input
                  type="text"
                  id="budget"
                  name="budget"
                  placeholder="Budget"
                  value={newItem.budget}
                  error={errorType.budget}
                  onBlur={handleBlur}
                  onChange={handleInputChange}
                />
              </div>
              <ModalButtons handleToggleModal={handleToggleModal} />
            </form>
          </div>
        </div>
        <div id="overlay" className={styles.overlay}></div>
      </div>
    );
  },
  (prevProps, nextProps) =>
    JSON.stringify(prevProps) !== JSON.stringify(nextProps)
);

export default CreateCampaignsItemModal;
