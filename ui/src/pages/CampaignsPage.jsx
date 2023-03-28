import { useState, useCallback } from "react";
import { useCampaigns } from "../hooks/useCampaigns";
import CreateCampaignsItemModal from "../components/CreateCampaignsItemModal";
import CampaignsTableItems from "../components/CampaignsTableItems";
import Button from "../components/Button/Button";
import Header from "../components/Header/Header";
import Spinner from "../components/Spinner/Spinner";
import Error from "../components/Error/Error";
import styles from "../styles/Campaigns.module.css";

const CampaignsPage = () => {
  const [isOpenModal, setIsOpenModal] = useState(false);
  const {
    isLoading,
    isError,
    campaigns,
    removeCampaign,
    createCampaign,
    handleCheckboxChange,
  } = useCampaigns();

  const toggleModal = useCallback(() => {
    setIsOpenModal((isOpenModal) => !isOpenModal);
  }, []);

  if (isLoading) {
    return <Spinner />;
  }

  if (isError) {
    return <Error />;
  }

  return (
    <div className={styles.campaignsWrapper}>
      <div className={styles.container}>
        <Header text="Campaigns" />
        <div className={styles.createButtonWrapper}>
          <Button handleClick={toggleModal} text="Create" />
        </div>
        <div className={styles.row}>
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Budget</th>
                  <th className={styles.centered}>Active</th>
                  <th className={styles.centered}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {campaigns.map((item) => {
                  return (
                    <CampaignsTableItems
                      key={item.id}
                      item={item}
                      handleRemove={() => removeCampaign.mutate(item.id)}
                      handleCheckboxChange={(item) =>
                        handleCheckboxChange.mutate(item)
                      }
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
          handleToggleModal={toggleModal}
          handleCreateCampaignsItem={(formValues, configure) => {
            if (+configure[0].budget >= formValues.budget) {
              createCampaign.mutate(formValues);
            }
          }}
        />
      )}
    </div>
  );
};

export default CampaignsPage;
