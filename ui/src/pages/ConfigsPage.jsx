import styles from "../styles/Config.module.css";
import axios from "axios";
import { useEffect, useState } from "react";
import PageNavigations from '../components/PageNavigations';

const ConfigsPage = () => {
    const [configs, setConfigs] = useState({});

  useEffect(() => {
    axios.get("http://localhost:8000/game/configure/")
        .then((response) => {
            if(response.status === 200) {
                const currentObject = response.data.find(obj => obj.current === true);
                setConfigs(currentObject);
            }
        })
        .catch((error) => {
            console.error(error);
        });
  }, []);
console.log(configs)
  return (
    <div className={styles.configsWrapper}>
         <ul>
            <li>Action type: {configs.auction_type}</li>
            <li>Budget: {configs.budget}</li>
            <li>Click revenue: {configs.click_revenue}</li>
            <li>Conversion revenue: {configs.conversion_revenue}</li>
            <li>Created at: {configs.created_at}</li>
            <li>Current: {configs.current}</li>
            <li>Frequency capping: {configs.frequency_capping}</li>
            <li>Id: {configs.id}</li>
            <li>Impression revenue: {configs.impression_revenue}</li>
            <li>Impressions total: {configs.impressions_total}</li>
            <li>Mode: {configs.mode}</li>
            <li>Rounds left: {configs.rounds_left}</li>
         </ul>
    </div>
  );
};

export default ConfigsPage;
