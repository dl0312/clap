import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.scss";
import PostActions from "components/PostActions";
import PostComments from "components/PostComments";
import TimeStamp from "components/TimeStamp";
import CommentBox from "components/CommentBox";
import UserList from "components/UserList";

const FeedPost = (props, context) => {
  return (
    <div className={styles.feedPost}>
      <header className={styles.header}>
        <span className={styles.category}>{props.category.name}</span>
        <span className={styles.title}>{props.title}</span>
        <TimeStamp time={props.natural_time} />
        <div className={styles.headerColumn}>
          <img
            src={props.creator.profile_image || require("images/noPhoto.jpg")}
            alt={props.creator.username}
            className={styles.image}
          />
          <span className={styles.creator}>{props.creator.username}</span>
        </div>
      </header>
      <span className={styles.body}>{props.body}</span>
      <div className={styles.meta}>
        <PostActions
          number={props.clap_count}
          isClaped={props.is_claped}
          postId={props.id}
          openClaps={props.openClaps}
        />
        <PostComments
          creator={props.creator.username}
          comments={props.comments}
        />
        <CommentBox photoId={props.id} />
      </div>
      {props.seeingClaps && (
        <UserList title={context.t("Claps")} closeLikes={props.closeClaps} />
      )}
    </div>
  );
};

FeedPost.contextTypes = {
  t: PropTypes.func.isRequired
};

FeedPost.propTypes = {
  id: PropTypes.number.isRequired,
  creator: PropTypes.shape({
    profile_image: PropTypes.string,
    username: PropTypes.string.isRequired
  }).isRequired,
  body: PropTypes.string.isRequired,
  clap_count: PropTypes.number.isRequired,
  comments: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      message: PropTypes.string.isRequired,
      creator: PropTypes.shape({
        profile_image: PropTypes.string,
        username: PropTypes.string.isRequired
      }).isRequired
    })
  ).isRequired,
  natural_time: PropTypes.string.isRequired,
  is_claped: PropTypes.bool.isRequired,
  seeingClaps: PropTypes.bool.isRequired,
  openClaps: PropTypes.func.isRequired,
  closeClaps: PropTypes.func.isRequired
};

export default FeedPost;
