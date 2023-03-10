import React from "react";
import "../styles/campaign.css";

const TableItems = ({ item, handleEdit, handleRemove }) => {
  return (
    <tr>
      <th scope="row">{item.id}</th>
      <td>{item.name}</td>
      <td>{item.budget}</td>
      <td>
        <button
          className="editCampaignsItem"
          onClick={() => handleEdit(item.id)}
        >
          Edit
        </button>
        <button
          className="removeCampaignsItem"
          onClick={() => handleRemove(item.id)}
        >
          Remove
        </button>
      </td>
    </tr>
  );
};

export default TableItems;
