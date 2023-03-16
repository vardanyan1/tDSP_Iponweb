import { useEffect, useState } from "react";
import styles from "../styles/CreativesItemModal.module.css";
import ImageUploadButton from "./ImageUploadButton";
import ModalButtons from "./ModalButtons";

const CreateCreativesItemModal = ({
  handleToggleModal,
  handleCreateCreativesItem,
}) => {
  const [newItem, setNewItem] = useState({
    name: "",
    external_id: "",
    categories: [],
    campaign: "",
    file: "",
  });
  const [errorType, setErrorType] = useState({
    name: false,
    external_id: false,
    categories: false,
    campaign: false,
    file: false,
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
    const { name, external_id, categories, campaign, file } = newItem;

    if (!name || !external_id || !categories.length || !campaign || !file) {
      setErrorType({
        name: !name,
        external_id: !external_id,
        categories: !categories.length,
        campaign: !campaign,
        file: !file,
      });
      return;
    }

    handleCreateCreativesItem(newItem);
  };

  const handleChooseImage = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = (event) => {
      const file = event.target.result;

      setNewItem((prevState) => ({ ...prevState, file }));

      setErrorType((prevState) => ({
        ...prevState,
        file: !file,
      }));
    };

    reader.readAsDataURL(file);
  };

  const handleSelectChange = (event) => {
    const { name, value } = event.target;

    setNewItem((prevState) => ({
      ...prevState,
      [name]: value,
    }));
    setErrorType((prevState) => ({
      ...prevState,
      [name]: !value,
    }));
  };

  return (
    <div>
      <div id="modal" className={styles.modal}>
        <div className={styles.modalContent}>
          <form onSubmit={handleSubmit} className={styles.createCreativesModal}>
            <div className={styles.inputsWrapper}>
              <input
                type="text"
                id="name"
                name="name"
                placeholder="Creative name"
                value={newItem.name}
                style={{
                  borderColor: errorType.name ? "#ff59a7" : undefined,
                }}
                onBlur={handleBlur}
                onChange={handleInputChange}
              />
              <input
                type="text"
                id="external_id"
                name="external_id"
                placeholder="External ID"
                value={newItem.external_id}
                style={{
                  borderColor: errorType.external_id ? "#ff59a7" : undefined,
                }}
                onBlur={handleBlur}
                onChange={handleInputChange}
              />
              <input
                type="text"
                id="categories"
                name="categories"
                placeholder="categories"
                value={newItem.categories}
                style={{
                  borderColor: errorType.categories ? "#ff59a7" : undefined,
                }}
                onBlur={handleBlur}
                onChange={handleInputChange}
              />
              <select
                id="campaign"
                name="campaign"
                className={styles.selectCampaign}
                onChange={handleSelectChange}
                style={{
                  borderColor: errorType.campaign ? "#ff59a7" : undefined,
                }}
              >
                {[1, 2, 3].map((item, index) => {
                  return (
                    <option key={index} value={item}>
                      {item}
                    </option>
                  );
                })}
              </select>
              <div className={styles.chooseImageBtnWrapper}>
                <ImageUploadButton
                  handleChooseImage={handleChooseImage}
                  file={newItem.file}
                />
              </div>
              <input
                type="text"
                id="file"
                name="file"
                placeholder="file"
                value={newItem.file}
                style={{
                  borderColor: errorType.file ? "#ff59a7" : undefined,
                }}
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
};

export default CreateCreativesItemModal;
