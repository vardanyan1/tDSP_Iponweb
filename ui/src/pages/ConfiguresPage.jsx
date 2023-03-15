import { useEffect, useState } from "react";
import axios from "../axios-instance";
import styles from "../styles/Configures.module.css";

const ConfiguresPage = () => {
  const [configures, setConfigures] = useState({});

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get("/game/configure/");
        if (response.status === 200) {
          const currentObject = response.data.find(
            (obj) => obj.current === true
          );
          setConfigures(currentObject);
        }
      } catch (error) {
        console.error(error);
      }
    }
    fetchData();
  }, []);

  const configItems = [
    { label: "Id", value: configures.id },
    { label: "Mode", value: configures.mode },
    { label: "Action type", value: configures.auction_type },
    { label: "Current", value: configures.current },
    { label: "Budget", value: configures.budget },
    { label: "Rounds left", value: configures.rounds_left },
    { label: "Frequency capping", value: configures.frequency_capping },
    { label: "Click revenue", value: configures.click_revenue },
    { label: "Conversion revenue", value: configures.conversion_revenue },
    { label: "Impression revenue", value: configures.impression_revenue },
    { label: "Impressions total", value: configures.impressions_total },
    { label: "Created at", value: configures.created_at },
  ];

  return (
    <>
      <h2 className={styles.headerText}>Configure</h2>
      <div className={styles.configuresWrapper}>
        <ul className={styles.configuresList}>
          {configItems.map((item, index) => (
            <li key={index}>
              <span>{item.label}</span>: {item.value}
            </li>
          ))}
        </ul>
      </div>
    </>
  );
};

export default ConfiguresPage;
