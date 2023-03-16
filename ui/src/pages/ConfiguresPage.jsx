import { useState } from "react";
import Header from "../components/Header/Header";
import { useFetchGetData } from "../hooks/useFetchData";
import styles from "../styles/Configures.module.css";

const ConfiguresPage = () => {
  const [configures, setConfigures] = useState({});

  const { isLoading, isError } = useFetchGetData(
    "/api/configure/",
    setConfigures
  );

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
    <div className={styles.configuresWrapper}>
      <div className={styles.container}>
        <Header text="Configure" />
        {isLoading && <p>Loading...</p>}
        {isError && <p>Error fetching data.</p>}
        {!isLoading && !isError && (
          <div className={styles.configuresWrapper}>
            <ul className={styles.configuresList}>
              {configItems.map((item, index) => (
                <li key={index}>
                  <span>{item.label}</span>: {item.value}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConfiguresPage;
