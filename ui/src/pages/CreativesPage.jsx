import { useState, useCallback } from "react";
import { useCreatives } from "../hooks/useCreatives";
import CreativesTableItems from "../components/CreativesTableItems";
import CreateCreativesItemModal from "../components/CreateCreativesItemModal";
import Header from "../components/Header/Header";
import Button from "../components/Button/Button";
import Spinner from "../components/Spinner/Spinner";
import Error from "../components/Error/Error";
import styles from "../styles/Creatives.module.css";

const CreativesPage = () => {
  const [isOpenModal, setIsOpenModal] = useState(false);
  const { isLoading, isError, creatives, removeCreative, createCreative } =
    useCreatives();

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
    <div className={styles.creativesWrapper}>
      <div className={styles.container}>
        <Header text="Creatives" />
        <div className={styles.createButtonWrapper}>
          <Button handleClick={toggleModal} text="Create" />
        </div>
        <div className={styles.row}>
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>External ID</th>
                  <th>Name</th>
                  <th>Categories</th>
                  <th>Campaign</th>
                  <th>Url</th>
                  <th className={styles.centered}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {creatives.map((item) => {
                  return (
                    <CreativesTableItems
                      key={item.id}
                      item={item}
                      handleRemove={() => removeCreative.mutate(item.id)}
                    />
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {isOpenModal && (
        <CreateCreativesItemModal
          handleToggleModal={toggleModal}
          handleCreateCreativesItem={(formValues) =>
            createCreative.mutate(formValues)
          }
        />
      )}
    </div>
  );
};

export default CreativesPage;
