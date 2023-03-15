import React from "react";
import styles from "../styles/Campaigns.module.css";

const TableItems = React.memo(
  ({ item, handleRemove }) => {
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
  },
  (prevProps, nextProps) =>
    JSON.stringify(prevProps) !== JSON.stringify(nextProps)
);

export default TableItems;
