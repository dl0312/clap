import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.scss";
import TimeStamp from "components/TimeStamp";

const PostList = (props, context) => {
  return (
    <div className={styles.postList}>
      <table className={styles.table}>
        <tr className={styles.tableRow}>
          <th classNmae={styles.tableCategory}>CATEGORY</th>
          <th className={styles.tableTitle}>TITLE</th>
          <th className={styles.tableCreator}>CREATOR</th>
          <th className={styles.tableCount}>COUNT</th>
          <th className={styles.tableDate}>DATE</th>
        </tr>
        {props.posts.map(post => (
          <tr className={styles.tableRow}>
            <td className={styles.tableCategory}>{post.category.name}</td>
            <td className={styles.tableTitle}>{post.title}</td>
            <td className={styles.tableCreator}>{post.username}</td>
            <td className={styles.tableCount}>
              <span className={styles.count}>{post.clap_count}</span>
              <span className={styles.count}>{post.comment_count}</span>
            </td>
            <td className={styles.tableDate}>
              <TimeStamp time={post.natural_time} />
            </td>
          </tr>
        ))}
      </table>
    </div>
  );
};

const Post = props => (
  <div className={styles.postElement}>
    <tr className={styles.tableRow}>
      <td className={styles.tableCategory}>{props.category}</td>
      <td className={styles.tableTitle}>{props.title}</td>
      <td className={styles.tableCreator}>{props.username}</td>
      <td className={styles.tableCount}>
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
