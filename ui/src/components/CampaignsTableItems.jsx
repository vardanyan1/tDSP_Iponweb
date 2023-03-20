import React from "react";
import styles from "../styles/Campaigns.module.css";
import Button from "./Button/Button";

const TableItems = React.memo(
  ({ item, handleRemove, handleCheckboxChange }) => {
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
          <input type="checkbox" checked={item.is_active} onChange={(e) => handleCheckboxChange(e, item)} />
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
    prevProps.item.id === nextProps.item.id &&
    prevProps.item.is_active === nextProps.item.is_active
);


export default TableItems;
