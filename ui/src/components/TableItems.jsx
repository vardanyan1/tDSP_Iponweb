import React from "react";
import styles from "../styles/Campaign.module.css";

const TableItems = ({ item, handleRemove }) => {
  return (
    <tr>
      <th scope="row">{item.id}</th>
      <td>
        <span>{item.name}</span>
      </td>
      <td>
        <span>{item.budget}</span>
      </td>
      <td>
        <button
          className={styles.removeCampaignsItem}
          onClick={() => handleRemove(item.id)}
        >
          Remove
        </button>
      </td>
    </tr>
  );
};

export default TableItems;
