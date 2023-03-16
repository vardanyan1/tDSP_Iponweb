import { useCallback, useState } from "react";
import styles from "../styles/Campaigns.module.css";
import CreateCampaignsItemModal from "../components/CreateCampaignsItemModal";
import CampaignsTableItems from "../components/CampaignsTableItems";
import Header from "../components/Header/Header";
import Button from "../components/Button/Button";
import { useFetchGetData } from "../hooks/useFetchData";

const CampaignsPage = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [isOpenModal, setIsOpenModal] = useState(false);

  const { isLoading, isError } = useFetchGetData(
    "/api/campaigns/",
    setCampaigns
  );

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
        <Header text="Campaigns" />
        <div className={styles.createButtonWrapper}>
          <Button handleClick={handleToggleModal} text="Create" />
        </div>
        <div className={styles.row}>
          <div className={styles.tableWrapper}>
            {isLoading ? (
              <p>Loading...</p>
            ) : isError ? (
              <p>Error: {isError}</p>
            ) : (
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
            )}
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
