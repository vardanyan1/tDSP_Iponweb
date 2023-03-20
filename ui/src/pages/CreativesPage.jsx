import { useState, useCallback } from "react";
import styles from "../styles/Creatives.module.css";
import CreativesTableItems from "../components/CreativesTableItems";
import CreateCreativesItemModal from "../components/CreateCreativesItemModal";
import Header from "../components/Header/Header";
import Button from "../components/Button/Button";
import { useFetchGetData } from "../hooks/useFetchData";
import axios from '../axios-instance';

const CreativesPage = () => {
  const [creatives, setCreatives] = useState([]);
  const [isOpenModal, setIsOpenModal] = useState(false);

  const { isLoading, isError } = useFetchGetData(
    "/api/creatives/",
    setCreatives
  );

  const handleRemove = useCallback((id) => {
  const access_token = localStorage.getItem('access');

  axios
    .delete(`/api/creatives/${id}`, { headers: { Authorization: `Bearer ${access_token}` } })
    .then((response) => {
      setCreatives((prevCreatives) =>
        prevCreatives.filter((creative) => creative.id !== id)
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

  const handleCreateCreativesItem = useCallback(
    (categories, newItem) => {

    const formattedCategories = categories
        .trim()
        .split(" ")
        .map((category) => ({ code: category }));

    const item = {...newItem, categories: formattedCategories};
    const access_token = localStorage.getItem('access');

    axios
     .post('/api/creatives/', item, { headers: { Authorization: `Bearer ${access_token}` } })
     .then((response) => {
          setCreatives((prevCreatives) => [...prevCreatives,  response.data ]);
     });

      handleToggleModal();
    },
    [handleToggleModal]
  );

  return (
    <div className={styles.creativesWrapper}>
      <div className={styles.container}>
        <Header text="Creatives" />
        <div className={styles.createButtonWrapper}>
          <Button handleClick={handleToggleModal} text="Create" />
        </div>
        <div className={styles.row}>
          <div className={styles.tableWrapper}>
            {isError && <div>Error loading data.</div>}
            {isLoading && <div>Loading...</div>}
            {!isError && !isLoading && (
              <table className={styles.table}>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>External ID</th>
                    <th>Name</th>
                    <th>Categories</th>
                    <th>Campaign</th>
                    <th>Url</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {creatives.map((item) => {
                    return (
                      <CreativesTableItems
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
        <CreateCreativesItemModal
          handleToggleModal={handleToggleModal}
          handleCreateCreativesItem={handleCreateCreativesItem}
        />
      )}
    </div>
  );
};

export default CreativesPage;
