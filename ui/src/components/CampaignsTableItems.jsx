import React, { useState } from "react";
import { useCallback } from "react";
import styles from "../styles/Campaigns.module.css";
import Button from "./Button/Button";

const TableItems = React.memo(
  ({ item, handleRemove, handleCheckboxChange, handleSubmitMinBid }) => {
    const [minBid, setMinBid] = useState(item.min_bid || "");

    const memoizedHandleRemove = useCallback(() => {
      handleRemove(item.id);
    }, [handleRemove, item.id]);

    const memoizedHandleCheckboxChange = useCallback(() => {
      handleCheckboxChange(item);
    }, [handleCheckboxChange, item]);

    const handleMinBidChange = (e) => {
      const value = e.target.value;

      if (value.length) {
        const regex = /^[0-9]+$/;
        const isNumber = regex.test(value);
        if (!isNumber) return;
      }

      setMinBid(value);
    };

    return (
      <tr>
        <th scope="row">{item.id}</th>
        <td>
          <span>{item.name}</span>
        </td>
        <td>
          <span>{item.budget}</span>
        </td>
        <td className={styles.centered}>
          <input
            type="checkbox"
            className={styles.customCheckbox}
            checked={item.is_active}
            onChange={() => memoizedHandleCheckboxChange(item)}
          />
        </td>
        <td className={styles.centered} style={{ width: "190px" }}>
          <div className={styles.minBidWrapper}>
            <input
              className={styles.minBidInput}
              name="minBid"
              placeholder="MinBid"
              value={minBid}
              onChange={(e) => handleMinBidChange(e)}
            />
            <button
              className={styles.minBidButton}
              onClick={() =>
                handleSubmitMinBid({ ...item, min_bid: minBid || null })
              }
            >
              Submit
            </button>
          </div>
        </td>
        <td className={styles.centered}>
          <div className={styles.removeBtnWrapper}>
            <Button
              handleClick={() => memoizedHandleRemove(item.id)}
              text="Remove"
            />
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
