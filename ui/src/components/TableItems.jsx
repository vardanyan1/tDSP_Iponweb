import React from "react";
import styles from "../styles/Campaign.module.css";

const TableItems = ({
  item,
  handleIsEdited,
  handleRemove,
  isEdited,
  handleChangeName,
  handleChangeBudget,
}) => {
  return (
    <tr>
      <th scope="row">{item.id}</th>
      <td>
        <input
          className={`${styles.campaignsInputs} ${
            item.isDisabled ? "" : styles.editedItemBorderColor
          }`}
          disabled={item.isDisabled}
          value={item.name}
          onChange={(e) => handleChangeName(e, item.id)}
        />
      </td>
      <td>
        <input
          className={`${styles.campaignsInputs} ${
            item.isDisabled ? "" : styles.editedItemBorderColor
          }`}
          disabled={item.isDisabled}
          value={item.budget}
          onChange={(e) => handleChangeBudget(e, item.id)}
        />
      </td>
      <td>
        <button
          className={styles.editCampaignsItem}
          onClick={() => handleIsEdited(item.id)}
        >
          {item.isDisabled ? "Edit" : "Save"}
        </button>
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
