import { useCallback, useEffect, useState } from "react";
import axios from "../axios-instance";
import styles from "../styles/Campaigns.module.css";
import CreateCampaignsItemModal from "../components/CreateCampaignsItemModal";
import CampaignsTableItems from "../components/CampaignsTableItems";

const initialState = [{ id: 100, name: "test", budget: "100000000" }];

const CampaignsPage = () => {
  const [campaigns, setCampaigns] = useState(initialState);
  const [isOpenModal, setIsOpenModal] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get("/api/campaigns/");
        if (response.status === 200) {
          setCampaigns(response.data);
        }
      } catch (error) {
        console.error(error);
      }
    }
    fetchData();
  }, []);

  const handleRemove = useCallback((id) => {
    setCampaigns((prevCampaigns) =>
      prevCampaigns.filter((campaign) => campaign.id !== id)
    );
  }, []);

  const handleToggleModal = useCallback(
    () => setIsOpenModal(!isOpenModal),
    [isOpenModal]
  );

  const handleCreateCampaignsItem = useCallback(
    (formValues) => {
      // Clear in Feature
      const lastId = campaigns[campaigns.length - 1]?.id || 0;
      setCampaigns((prevCampaigns) => [
        ...prevCampaigns,
        { id: lastId + 1, ...formValues },
      ]);
      handleToggleModal();
    },
    [campaigns, handleToggleModal]
  );

  return (
    <div className={styles.campaignsWrapper}>
      <div className={styles.container}>
        <div className={styles.row}>
          <div className={styles.headerWrapper}>
            <h2>Campaigns</h2>
          </div>
        </div>
        <div className={styles.createButtonWrapper}>
          <button onClick={handleToggleModal}>Create</button>
        </div>
        <div className={styles.row}>
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
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
                    <CampaignsTableItems
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

      {isOpenModal && (
        <CreateCampaignsItemModal
          handleToggleModal={handleToggleModal}
          handleCreateCampaignsItem={handleCreateCampaignsItem}
        />
      )}
    </div>
  );
};

export default CampaignsPage;
