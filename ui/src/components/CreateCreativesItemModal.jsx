import { useEffect, useState } from "react";
import { useFetchGetData } from "../hooks/useFetchData";
import styles from "../styles/CreativesItemModal.module.css";
import ImageUploadButton from "./ImageUploadButton";
import Input from "./Input";
import ModalButtons from "./ModalButtons";

const CreateCreativesItemModal = ({
  handleToggleModal,
  handleCreateCreativesItem,
}) => {
  const [newItem, setNewItem] = useState({
    name: "",
    external_id: "",
    categories: [],
    campaign: { id: null, name: "" },
    file: "",
  });
  const [errorType, setErrorType] = useState({
    name: false,
    external_id: false,
    categories: false,
    campaign: false,
    file: false,
  });
  const [campaigns, setCampaigns] = useState([]);

  const { isLoading, isError } = useFetchGetData(
    "/api/campaigns/",
    setCampaigns
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
    console.log(campaign);
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
    const { value, id } = event.target;

    setNewItem((prevItem) => ({
      ...prevItem,
      campaign: { id: id, name: value },
    }));
    setErrorType((prevItem) => ({
      ...prevItem,
      campaign: !value,
    }));
  };

  return (
    <div>
      <div id="modal" className={styles.modal}>
        <div className={styles.modalContent}>
          {isLoading ? (
            <p>Loading...</p>
          ) : isError ? (
            <p>Error: {isError}</p>
          ) : (
            <form
              onSubmit={handleSubmit}
              className={styles.createCreativesModal}
            >
              <div className={styles.inputsWrapper}>
                <Input
                  id="name"
                  name="name"
                  type="text"
                  placeholder="Creative name"
                  value={newItem.name}
                  onBlur={handleBlur}
                  onChange={handleInputChange}
                  error={errorType.name}
                />
                <Input
                  id="external_id"
                  name="external_id"
                  placeholder="External ID"
                  value={newItem.external_id}
                  onBlur={handleBlur}
                  onChange={handleInputChange}
                  error={errorType.external_id}
                />
                <Input
                  id="categories"
                  name="categories"
                  placeholder="categories"
                  value={newItem.categories}
                  onBlur={handleBlur}
                  onChange={handleInputChange}
                  error={errorType.categories}
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
                  {campaigns.map((item, index) => {
                    return (
                      <option key={index} id={item.id} value={item.name}>
                        {item.name}
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
          )}
        </div>
      </div>
      <div id="overlay" className={styles.overlay}></div>
    </div>
  );
};

export default CreateCreativesItemModal;
