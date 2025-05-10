import { useState } from "react";

import { deletePost, updatePost } from "../util/BlogHttp";

import styles from "./Post.module.css";

function Post({ data, refreshDeta }) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(data.title);
  const [content, setContent] = useState(data.content);
  const [modifiedTime, setModifiedTime] = useState(data.last_modified);
  function editPost() {
    setIsEditing(true);
  }

  function cancelEdit() {
    setIsEditing(false);
  }

  function deletePostHandle() {
    deletePost(data.id)
      .then(() => {
        refreshDeta();
      })
      .catch((error) => {
        alert(error);
      });
  }

  function editPostHandle() {
    const post = {
      id: data.id,
      title,
      content,
    };
    updatePost(post)
      .then((res) => {
        setContent(res.content.replace(/ /g, "\u00A0"));
        setTitle(res.title.replace(/ /g, "\u00A0"));
        setModifiedTime(res.last_modified);
        setIsEditing(false);
      })
      .catch((error) => {
        alert(error);
      });
  }

  return (
    <>
      <div className={styles.postCard}>
        {isEditing ? (
          <>
            <div className={styles.form}>
              <input
                type="text"
                name="title"
                value={title}
                placeholder="Title"
                className={styles.titleInput}
                onChange={(e) => setTitle(e.target.value)}
              />
              <textarea
                name="content"
                placeholder="Message"
                className={styles.contentInput}
                value={content}
                onChange={(e) => setContent(e.target.value)}
              ></textarea>
            </div>
            <button
              type="button"
              onClick={editPostHandle}
              className={styles.editButton}
            >
              done
            </button>
            <button
              type="button"
              onClick={cancelEdit}
              className={styles.removeButton}
            >
              cancel
            </button>
          </>
        ) : (
          <>
            <h3 className={styles.titlePost}>
              {title.replace(/ /g, "\u00A0")}
            </h3>
            <p className={styles.contentPost}>
              {content.replace(/ /g, "\u00A0")}
            </p>
            <button
              type="button"
              onClick={editPost}
              className={styles.editButton}
            >
              Edit
            </button>
            <button
              type="button"
              onClick={deletePostHandle}
              className={styles.removeButton}
            >
              Remove
            </button>
          </>
        )}
        <p className={styles.timestamp}>
          <span>Last modified: {modifiedTime}</span>
          <span style={{ marginLeft: "1rem" }}>
            Created at: {data.created_at}
          </span>
        </p>
      </div>
    </>
  );
}
export default Post;
