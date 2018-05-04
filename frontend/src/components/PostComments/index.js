import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.scss";

const PostComments = props => (
  <div className={styles.comments}>
    <ul className={styles.list}>
      {props.comments.map(comment => (
        <Comment
          username={comment.creator.username}
          comment={comment.message}
          key={comment.id}
        />
      ))}
    </ul>
  </div>
);

const Comment = props => (
  <li className={styles.comment}>
    <span className={styles.username}>{props.username}</span>{" "}
    <span className={styles.message}>{props.comment}</span>
  </li>
);

PostComments.propTypes = {
  creator: PropTypes.string.isRequired,
  comments: PropTypes.arrayOf(
    PropTypes.shape({
      message: PropTypes.string.isRequired,
      creator: PropTypes.shape({
        profile_image: PropTypes.string,
        username: PropTypes.string.isRequired
      }).isRequired
    })
  ).isRequired
};

export default PostComments;
