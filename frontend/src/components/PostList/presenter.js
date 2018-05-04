import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.scss";
import TimeStamp from "components/TimeStamp";

const PostList = (props, context) => {
  return (
    <div className={styles.postList}>
      <table className={styles.table}>
        <div className={styles.postElements}>
          <tr className={styles.tableRow}>
            <th className={styles.tabelHead}>ID</th>
            <th className={styles.tabelHead}>TITLE</th>
            <th className={styles.tabelHead}>CREATOR</th>
            <th className={styles.tabelHead}>COUNT</th>
            <th className={styles.tabelHead}>DATE</th>
          </tr>

          {props.posts.map(post => (
            <Post
              id={post.id}
              title={post.title}
              username={post.creator.username}
              clap_count={post.clap_count}
              comment_count={post.comment_count}
              natural_time={post.natural_time}
              key={post.id}
            />
          ))}
        </div>
      </table>
    </div>
  );
};

const Post = props => (
  <div className={styles.post}>
    <tr className={styles.tableRow}>
      <td className={styles.tableData}>{props.id}</td>
      <td className={styles.tableData}>{props.title}</td>
      <td className={styles.tableData}>{props.username}</td>
      <td className={styles.tableData}>
        <span className={styles.count}>{props.clap_count}</span>
        <span className={styles.count}>{props.comment_count}</span>
      </td>
      <td className={styles.tableData}>
        <TimeStamp time={props.natural_time} />
      </td>
    </tr>
  </div>
);

export default PostList;
