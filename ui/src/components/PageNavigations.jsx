import React, { useState } from "react";
import styles from "../styles/Navigations.module.css";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

const PageNavigations = () => {
  return (
    <div className={styles.navigationLinksWrapper}>
      <Link to='/campaigns'>Campaigns</Link>
      <Link to='/creatives'>Creatives</Link>
      <Link to='/config'>Config</Link>
    </div>
  );
};

export default PageNavigations;
