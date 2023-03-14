import styles from "../styles/Campaign.module.css";
import CreateCampaignItemModal from "../components/CreateCampaignItemModal";
import TableItems from "../components/TableItems";
import axios from "axios";
import { useEffect, useState } from "react";
import { useRef } from "react";
import PageNavigations from '../components/PageNavigations';

const CampaignsPage = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [isOpenModal, setIsOpenModal] = useState(false);
  const modalRef = useRef(null);

  useEffect(() => {
    axios.get("http://localhost/api/campaigns").then((response) => {
      setCampaigns(response.data);
    });
  }, []);

  const handleIsEdited = (id) => {
    setCampaigns((prevCampaigns) =>
      prevCampaigns.map((campaign) =>
        campaign.id === id
          ? { ...campaign, isDisabled: !campaign.isDisabled }
          : campaign
      )
    );
  };

  const handleChangeName = (e, id) => {
    setCampaigns((prevCampaigns) =>
      prevCampaigns.map((campaign) =>
        campaign.id === id ? { ...campaign, name: e.target.value } : campaign
      )
    );
  };
  const handleChangeBudget = (e, id) => {
    const regex = /^[0-9]+$/;
    const isNumber = regex.test(e.target.value);

    if (isNumber || e.target.value === "") {
      setCampaigns((prevCampaigns) =>
        prevCampaigns.map((campaign) =>
          campaign.id === id
            ? { ...campaign, budget: e.target.value }
            : campaign
        )
      );
    }
  };

  const handleRemove = (id) => {
    setCampaigns((prevCampaigns) =>
      prevCampaigns.filter((campaign) => campaign.id !== id)
    );
  };

  const handleToggleModal = () => {
    setIsOpenModal(!isOpenModal);
  };

  const handleCreateCampaignItem = (formValues) => {
    // Clear in Feature
    const lastId = campaigns.at(-1)?.id || 0;
    setCampaigns((prevState) => [
      ...prevState,
      { id: lastId + 1, ...formValues },
    ]);
    handleToggleModal();
  };

  console.log({ campaigns });

  return (
    <div className={styles.tableWrapper}>
      <div className={styles.container}>
        <div className={`${styles.row} ${styles.justifyContentCenter}`}>
          <div
            className={`${styles.colMd6} ${styles.textCenter} ${styles.mb3}`}
          >
            <h2 className={styles.headingSection}>Campaigns</h2>
          </div>
        </div>
        <div className={styles.createCampaignWrapper}>
          <button onClick={handleToggleModal} className={styles.createCampaign}>
            Create
          </button>
        </div>
        <div className={styles.row}>
          <div className={styles.colMd12}>
            <div>
              <table
                className={`${styles.table} ${styles.tableBordered} ${styles.tableDark}`}
              >
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Budget</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {campaigns.map((item) => {
                    return (
                      <TableItems
                        key={item.id}
                        item={item}
                        handleIsEdited={handleIsEdited}
                        handleRemove={handleRemove}
                        handleChangeName={handleChangeName}
                        handleChangeBudget={handleChangeBudget}
                      />
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {isOpenModal && (
        <CreateCampaignItemModal
          handleToggleModal={handleToggleModal}
          modalRef={modalRef}
          handleCreateCampaignItem={handleCreateCampaignItem}
        />
      )}
    </div>
  );
};

export default CampaignsPage;
