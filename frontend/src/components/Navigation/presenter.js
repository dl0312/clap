import React from "react";
import PropTypes from "prop-types";
import Ionicon from "react-ionicons";
import { Link } from "react-router-dom";
import styles from "./styles.scss";

const Navigation = (props, context) => (
  <div className={styles.navigation}>
    <div className={styles.inner}>
      <div className={styles.column}>
        <Link to="/">
          <img
            src={require("images/claplogo.png")}
            className={styles.logo}
            alt={context.t("Logo")}
          />
        </Link>
      </div>
      <div className={styles.column}>
        <input
          type="text"
          placeholder={context.t("search")}
          className={styles.searchInput}
        />
      </div>
      <div className={styles.column}>
        <div className={styles.navIcon}>
          <Link to="/explore">
            <Ionicon icon="ios-compass-outline" />
          </Link>
        </div>
        <div className={styles.navIcon}>
          <Ionicon icon="ios-hand-outline" fontSize="28px" color="black" />
        </div>
        <div className={styles.navIcon}>
          <Link to="/profile">
            <Ionicon icon="ios-person-outline" fontSize="28px" color="black" />
          </Link>
        </div>
      </div>
    </div>
  </div>
);

Navigation.contextTypes = {
  t: PropTypes.func.isRequired
};

export default Navigation;
