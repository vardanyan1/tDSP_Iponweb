import { useConfigures } from "../hooks/useConfigures";
import Header from "../components/Header/Header";
import Spinner from "../components/Spinner/Spinner";
import Error from "../components/Error/Error";
import styles from "../styles/Configures.module.css";

const ConfiguresPage = () => {
  const { isLoading, isError, configItems } = useConfigures();

  if (isLoading) {
    return <Spinner />;
  }

  if (isError) {
    return <Error />;
  }

  return (
    <div className={styles.configuresWrapper}>
      <div className={styles.container}>
        <Header text="Configure" />
        <div className={styles.configuresWrapper}>
          <ul className={styles.configuresList}>
            {configItems.map((item, index) => (
              <li key={index}>
                <span>{item.label}</span>: {item.value}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ConfiguresPage;
