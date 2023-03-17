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
    campaign: null,
    url: "",
  });
  const [errorType, setErrorType] = useState({
    name: false,
    external_id: false,
    categories: false,
    campaign: false,
    url: false,
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

  const handleChooseImage = (e) => {
    const file = e.target.files[0];

    const reader = new FileReader();
    reader.onload = (event) => {
      const url = event.target.result;

      setNewItem((prevState) => ({ ...prevState, url }));

      setErrorType((prevState) => ({
        ...prevState,
        url: !url,
      }));
    };

    reader.readAsDataURL(file);
  };

  const handleSelectChange = (event) => {
    console.log(event);
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

  const handleSubmit = (event) => {
    event.preventDefault();
    const { name, external_id, categories, campaign, url } = newItem;
    console.log("external - ", external_id, "campaign - ", campaign);
    if (!name || !external_id || !categories.length || !campaign || !url) {
      setErrorType({
        name: !name,
        external_id: !external_id,
        categories: !categories.length,
        campaign: !campaign,
        url: !url,
      });
      return;
    }

    handleCreateCreativesItem(newItem);
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
                  <option
                    value=""
                    defaultValue
                    hidden
                    style={{ color: "#a0a0a0" }}
                  >
                    Select Campaign
                  </option>
                  {campaigns.map((item) => {
                    return (
                      <option key={item.id} id={item.id} value={item.name}>
                        {item.name}
                      </option>
                    );
                  })}
                </select>
                <div className={styles.chooseImageBtnWrapper}>
                  <ImageUploadButton
                    handleChooseImage={handleChooseImage}
                    url={newItem.url}
                  />
                </div>
                <input
                  type="text"
                  id="url"
                  name="url"
                  placeholder="url"
                  value={newItem.url}
                  readOnly
                  style={{
                    borderColor: errorType.url ? "#ff59a7" : undefined,
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
