import { useState } from "react";
import Error from "../components/Error/Error";
import Header from "../components/Header/Header";
import Spinner from "../components/Spinner/Spinner";
import { useFetchGetData } from "../hooks/useFetchData";
import styles from "../styles/Configures.module.css";

const ConfiguresPage = () => {
  const [configures, setConfigures] = useState({});

  const { isLoading, isError } = useFetchGetData(
    "/game/configure/",
    setConfigures
  );

  const formatDate = (dateString) => {
    const date = new Date(dateString);

    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();

    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    return `${day}/${month}/${year} ${hours}:${minutes}`;
  };

  const configItems = [
    { label: "Id", value: configures?.id },
    { label: "Mode", value: configures?.mode },
    { label: "Auction type", value: configures?.auction_type },
    { label: "Game goal", value: configures?.game_goal },
    { label: "Current", value: configures?.current + "" },
    { label: "Budget", value: configures?.budget },
    { label: "Rounds left", value: configures?.rounds_left },
    { label: "Frequency capping", value: configures?.frequency_capping },
    { label: "Click revenue", value: configures?.click_revenue },
    { label: "Conversion revenue", value: configures?.conversion_revenue },
    { label: "Impression revenue", value: configures?.impression_revenue },
    { label: "Impressions total", value: configures?.impressions_total },
    {
      label: "Created at",
      value: formatDate(configures?.created_at),
    },
  ];

  return (
    <div className={styles.configuresWrapper}>
      <div className={styles.container}>
        <Header text="Configure" />
        <div className={styles.configuresWrapper}>
          {isLoading && <Spinner />}
          {isError && <Error />}
          {!isLoading && !isError && (
            <ul className={styles.configuresList}>
              {configItems.map((item, index) => (
                <li key={index}>
                  <span>{item.label}</span>: {item.value}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default ConfiguresPage;
