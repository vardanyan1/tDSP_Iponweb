import styles from "../styles/Creatives.module.css";

const CreativesTableItems = ({ item, handleRemove }) => {
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
        {item?.categories?.map((item, index) => (
          <span key={item.code}>
            {index > 0 ? ", " + item.code : item.code}
          </span>
        ))}
        {/* {item?.categories} */}
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
      <td>
        <button
          className={styles.removeCreativesItem}
          onClick={() => handleRemove(item.id)}
        >
          Remove
        </button>
      </td>
    </tr>
  );
};

export default CreativesTableItems;
