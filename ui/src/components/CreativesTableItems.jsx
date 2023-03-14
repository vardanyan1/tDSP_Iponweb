import React from "react";
import styles from "../styles/Creatives.module.css";

const CreativesTableItems = ({
  item
}) => {
console.log(item)
  return (
    <tr>
      <th scope="row">{item.id}</th>
      <td>
        <span>{item.external_id}</span>
      </td>
      <td>
        <span>{item.name}</span>
      </td>
      <td>
      {item.categories.map((item, index) => {
        return (
            <span>{index > 0 ? ', ' + item.code : item.code}</span>
        )
       })
      }

      </td>
      <td>
        <span>{item.campaign.name}</span>
      </td>
      <td>
        <a href={item.url} className={styles.itemUrl}>{item.url}</a>
      </td>
      <td>
        <button
          className={styles.removeCampaignsItem}
        >
          Remove
        </button>
      </td>
    </tr>
  );
};

export default CreativesTableItems;
