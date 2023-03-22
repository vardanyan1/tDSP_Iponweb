import { useCallback, useState } from "react";
import styles from "../styles/Campaigns.module.css";
import CreateCampaignsItemModal from "../components/CreateCampaignsItemModal";
import CampaignsTableItems from "../components/CampaignsTableItems";
import Header from "../components/Header/Header";
import Button from "../components/Button/Button";
import { useFetchGetData } from "../hooks/useFetchData";
import axios from "../axios-instance";
import Spinner from "../components/Spinner/Spinner";
import Error from "../components/Error/Error";

const CampaignsPage = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [isOpenModal, setIsOpenModal] = useState(false);

  const { isLoading, isError } = useFetchGetData(
    "/api/campaigns/",
    setCampaigns
  );

  const handleRemove = useCallback((id) => {
    const access_token = localStorage.getItem("token");

    axios
      .delete(`/api/campaigns/${id}`, {
        headers: { Authorization: `Bearer ${access_token}` },
      })
      .then((response) => {
        setCampaigns((prevCampaigns) =>
          prevCampaigns.filter((campaign) => campaign.id !== id)
        );
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  const handleToggleModal = useCallback(
    () => setIsOpenModal(!isOpenModal),
    [isOpenModal]
  );

  const handleCreateCampaignsItem = useCallback(
    (formValues, configure) => {
      if (+configure.budget >= formValues.budget) {
        const access_token = localStorage.getItem("token");

        axios
          .post("/api/campaigns/", formValues, {
            headers: { Authorization: `Bearer ${access_token}` },
          })
          .then((response) => {
            setCampaigns((prevCampaigns) => [...prevCampaigns, response.data]);
          });

        handleToggleModal();
      }
    },
    [handleToggleModal]
  );

  const handleCheckboxChange = (e, item) => {
    const access_token = localStorage.getItem("token");

    axios
      .put(
        `/api/campaigns/${item.id}/`,
        { ...item, is_active: e.target.checked },
        { headers: { Authorization: `Bearer ${access_token}` } }
      )
      .then((response) => {
        setCampaigns((prevCampaigns) => {
          return prevCampaigns.map((campaign) => {
            if (campaign.id === item.id) {
              return { ...campaign, is_active: response.data.is_active };
            } else {
              return campaign;
            }
          });
        });
      });
  };
  return (
    <div className={styles.campaignsWrapper}>
      <div className={styles.container}>
        <Header text="Campaigns" />
        <div className={styles.createButtonWrapper}>
          <Button handleClick={handleToggleModal} text="Create" />
        </div>
        <div className={styles.row}>
          <div className={styles.tableWrapper}>
            {isLoading && <Spinner />}
            {isError && <Error />}
            {!isError && !isLoading && (
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
                        handleRemove={handleRemove}
                        handleCheckboxChange={handleCheckboxChange}
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
