import React from "react";
import PropTypes from "prop-types";
import Ionicon from "react-ionicons";
import styles from "./styles.scss";

const PostActions = (props, context) => (
  <div className={styles.actions}>
    <div className={styles.icons}>
      <span className={styles.icon} onClick={props.handleHeartClick}>
        {props.isClaped ? (
          <Ionicon icon="ios-heart" fontSize="28px" color="#EB4B59" />
        ) : (
          <Ionicon icon="ios-heart-outline" fontSize="28px" color="black" />
        )}
      </span>
      <span className={styles.icon}>
        <Ionicon icon="ios-text-outline" fontSize="28px" color="black" />
      </span>
    </div>
    <span className={styles.likes} onClick={props.openClaps}>
      {props.number}{" "}
      {props.number === 1 ? context.t("clap") : context.t("claps")}
    </span>
  </div>
);

PostActions.propTypes = {
  number: PropTypes.number.isRequired,
  isClaped: PropTypes.bool.isRequired,
  postId: PropTypes.number.isRequired,
  handleHeartClick: PropTypes.func.isRequired,
  openClaps: PropTypes.func.isRequired
};

PostActions.contextTypes = {
  t: PropTypes.func.isRequired
};

export default PostActions;
