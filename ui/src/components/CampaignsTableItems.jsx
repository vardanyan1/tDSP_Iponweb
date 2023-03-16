import React from "react";
import styles from "../styles/Campaigns.module.css";
import Button from "./Button/Button";

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
          <div className={styles.removeBtnWrapper}>
            <Button handleClick={() => handleRemove(item.id)} text="Remove" />
          </div>
        </td>
      </tr>
    );
  },
  (prevProps, nextProps) =>
    JSON.stringify(prevProps) !== JSON.stringify(nextProps)
);

export default TableItems;
