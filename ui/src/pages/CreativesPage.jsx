import { useState, useCallback } from "react";
import styles from "../styles/Creatives.module.css";
import CreativesTableItems from "../components/CreativesTableItems";
import CreateCreativesItemModal from "../components/CreateCreativesItemModal";
import Header from "../components/Header/Header";
import Button from "../components/Button/Button";
import { useFetchGetData } from "../hooks/useFetchData";

const CreativesPage = () => {
  const [creatives, setCreatives] = useState([]);
  const [isOpenModal, setIsOpenModal] = useState(false);

  const { isLoading, isError } = useFetchGetData(
    "/api/creatives/",
    setCreatives
  );

  const handleRemove = useCallback((id) => {
    setCreatives((prevCreatives) =>
      prevCreatives.filter((creative) => creative.id !== id)
    );
  }, []);

  const handleToggleModal = useCallback(
    () => setIsOpenModal(!isOpenModal),
    [isOpenModal]
  );

  const handleCreateCreativesItem = useCallback(
    (formValues) => {
      const categoryArray = formValues.categories
        .trim()
        .split(/\s+/)
        .map((category) => ({ code: category }));

      const newItem = { ...formValues, categories: categoryArray };
      // Clear in Feature
      const lastId = creatives.at(-1)?.id || 0;

      setCreatives((prevCreatives) => [
        ...prevCreatives,
        { id: lastId + 1, ...newItem },
      ]);

      handleToggleModal();
    },
    [creatives, handleToggleModal]
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
