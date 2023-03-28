import React, { useCallback } from "react";
import styles from "../styles/Creatives.module.css";
import Button from "./Button/Button";

const CreativesTableItems = React.memo(({ item, handleRemove }) => {
  const memoizedHandleRemove = useCallback(() => {
    handleRemove(item.id);
  }, [handleRemove, item.id]);

  const itemCategories = item.categories
    .map((item, index) => (index > 0 ? ", " + item.code : item.code))
    .join("");

  return (
    <tr className={styles.itemsWrapper}>
      <th scope="row">{item.id}</th>
      <td>
        <span>{item.external_id}</span>
      </td>
      <td>
        <span>{item.name}</span>
      </td>
      <td>
        <span>{itemCategories}</span>
      </td>
      <td>
        <span>{item.campaign.name}</span>
      </td>
      <td>
        <a
          href={item.url}
          className={styles.itemUrl}
          target="_blank"
          rel="noreferrer"
        >
          {item.url}
        </a>
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
});

export default CreativesTableItems;
