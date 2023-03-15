import styles from "../styles/Campaign.module.css";
import CreateCampaignItemModal from "../components/CreateCampaignItemModal";
import TableItems from "../components/TableItems";
import axios from "axios";
import { useEffect, useState } from "react";
import { useRef } from "react";

const initialState = [{ id: 100, name: "test", budget: "100000000" }];

const CampaignsPage = () => {
  const [campaigns, setCampaigns] = useState(initialState);
  const [isOpenModal, setIsOpenModal] = useState(false);
  const modalRef = useRef(null);

  useEffect(() => {
    axios.get("http://localhost:8000/api/campaigns/").then((response) => {
      if (response.status === 200) {
        setCampaigns(response.data);
      }
    });
  }, []);

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
                        handleRemove={handleRemove}
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
