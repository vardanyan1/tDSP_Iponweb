import React, { useEffect, useState } from "react";
import axios from "../axios-instance";
import { useQuery } from "react-query";
import Input from "./Input/Input";
import ModalButtons from "./ModalButtons";
import styles from "../styles/CampaignsItemModal.module.css";
import Spinner from "./Spinner/Spinner";
import Error from "./Error/Error";

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

    const {
      isLoading,
      isError,
      data: configure = [],
    } = useQuery(
      "configure",
      async () => {
        const { data } = await axios.get("/game/configure/");
        return data;
      },
      {
        refetchOnWindowFocus: false, // disable automatic refetching
      }
    );

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

      if (budget && +budget > configure[0]?.budget) {
        setErrorType({
          ...errorType,
          budget: true,
        });
        return;
      }

      handleCreateCampaignsItem(newItem, configure);
      handleToggleModal();
    };

    if (isLoading) {
      return <Spinner />;
    }

    if (isError) {
      return <Error />;
    }

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
                  name="name"
                  placeholder="Campaign name"
                  value={newItem.name}
                  error={errorType.name}
                  onBlur={handleBlur}
                  onChange={handleInputChange}
                />
                <Input
                  name="budget"
                  placeholder="Budget"
                  value={newItem.budget}
                  error={errorType.budget}
                  onBlur={handleBlur}
                  onChange={handleInputChange}
                />
              </div>
              <p className={styles.errorText}>
                {errorType.budget &&
                  +newItem.budget > +configure[0]?.budget &&
                  `Max budget is ${+configure[0]?.budget}`}
              </p>
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
