import styles from "../styles/Creatives.module.css";
import TableItems from "../components/TableItems";
import axios from "axios";
import { useEffect, useState, useRef } from "react";
import CreativesTableItems from '../components/CreativesTableItems';
import CreateCampaignItemModal from '../components/CreateCampaignItemModal';
import PageNavigations from '../components/PageNavigations';

const CreativesPage = () => {
  const [creatives, setCreatives] = useState([]);
  const [isOpenModal, setIsOpenModal] = useState(false);
  const modalRef = useRef(null);

  useEffect(() => {
    axios.get("http://localhost:8000/api/creatives")
        .then((response) => {
            if(response.status === 200) {
                console.log(response.data);
                setCreatives(response.data);
            }
        })
        .catch((error) => {
            console.error(error);
        });
  }, []);

  const handleToggleModal = () => {};

  return (
    <div className={styles.tableWrapper}>
      <div className={styles.container}>
        <div className={`${styles.row} ${styles.justifyContentCenter}`}>
          <div
            className={`${styles.colMd6} ${styles.textCenter} ${styles.mb3}`}
          >
            <h2 className={styles.headingSection}>Creatives</h2>
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
                    <th>External ID</th>
                    <th>Name</th>
                    <th>Categories</th>
                    <th>Campaign</th>
                    <th>Url</th>
                  </tr>
                </thead>
                <tbody>
                  {creatives.map((item) => {
                    return (
                      <CreativesTableItems
                        key={item.id}
                        item={item}
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
          modalRef={modalRef}
        />
      )}
    </div>
  );
};

export default CreativesPage;
