import { useEffect, useState, useRef, useCallback } from "react";
import axios from "../axios-instance";
import styles from "../styles/Creatives.module.css";
import CreativesTableItems from "../components/CreativesTableItems";
import CreateCreativesItemModal from "../components/CreateCreativesItemModal";

const initialState = [
  {
    id: 100,
    external_id: "string",
    name: "test",
    categories: [{ code: "IAB_7" }, { code: "IAB_1-11" }],
    campaign: { id: 100 },
    url: "string_url",
  },
];

const CreativesPage = () => {
  const [creatives, setCreatives] = useState(initialState);
  const [isOpenModal, setIsOpenModal] = useState(false);
  const modalRef = useRef(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get("/api/creatives");
        if (response.status === 200) {
          setCreatives(response.data);
        }
      } catch (error) {
        console.error(error);
      }
    }
    fetchData();
  }, []);

  const handleRemove = useCallback((id) => {
    setCreatives((prevCreatives) =>
      prevCreatives.filter((creative) => creative.id !== id)
    );
  }, []);

  const handleToggleModal = useCallback(
    () => setIsOpenModal(!isOpenModal),
    [isOpenModal]
  );

  const handleCreateCreativesItem = (formValues) => {
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
  };

  return (
    <div className={styles.creativesWrapper}>
      <div className={styles.container}>
        <div className={styles.row}>
          <div className={styles.headerWrapper}>
            <h2>Creatives</h2>
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
                      {...{ item, handleRemove }}
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
          handleToggleModal={handleToggleModal}
          modalRef={modalRef}
          handleCreateCreativesItem={handleCreateCreativesItem}
        />
      )}
    </div>
  );
};

export default CreativesPage;
