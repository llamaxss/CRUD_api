import { useState, useEffect } from "react";
import Post from "../components/Post";

import styles from "./Blog.module.css";

import { getAllPosts, createPost } from "../util/BlogHttp";

function Blog() {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  function handleSubmit(formData) {
    const title = formData.get("title");
    const content = formData.get("content");

    const post = {
      title,
      content,
    };
    createPost(post)
      .then(() => {
        fetchPosts();
      })
      .catch((error) => {
        console.error("Error creating post:", error);
      });
  }
  async function fetchPosts() {
    try {
      const allPosts = await getAllPosts();
      setPosts(allPosts);
    } catch (error) {
      console.error("Error fetching posts:", error);
    } finally {
      setIsLoading(false);
    }
  }
  useEffect(() => {
    fetchPosts();
  }, []);

  return (
    <>
      <form id="post-form" action={handleSubmit}>
        <div className={styles.form}>
          <input
            type="text"
            name="title"
            id="title"
            placeholder="Title"
            className={styles.titleInput}
          />
          <textarea
            name="content"
            id="content"
            placeholder="Message"
            className={styles.contentInput}
          ></textarea>
        </div>
        <button type="submit" className={styles.submitButton}>
          Submit
        </button>
      </form>
      <div>
        {isLoading ? <p>Loading...</p> : null}
        {!isLoading && posts.length !== 0 ? (
          posts.map((post) => (
            <Post key={post.id} data={post} refreshDeta={fetchPosts} />
          ))
        ) : !isLoading && posts.length === 0 ? (
          <p>There is no post here.</p>
        ) : null}
      </div>
    </>
  );
}

export default Blog;
