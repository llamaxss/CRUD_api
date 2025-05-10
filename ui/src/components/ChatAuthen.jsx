import React, { useState } from "react";

import { loginHandle, registerHandle } from "../util/ChatHttp";

function ChatAuthen({ onSubmit }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState("");

  function handleAction(formData) {
    const username = formData.get("username");
    const password = formData.get("password");

    if (mode === "login") {
      loginHandle(username, password)
        .then((res) => {
          onSubmit(res.username);
        })
        .catch((error) => {
          console.error("Error:", error);
          alert(error.message);
        });
    } else if (mode === "register") {
      registerHandle(username, password)
        .then((res) => {
          onSubmit(res.username);
        })
        .catch((error) => {
          console.error("Error:", error);
          alert(error.message);
        });
    }
  }

  return (
    <div>
      <h1>Login</h1>
      <form action={(formData) => handleAction(formData, "login")}>
        <input
          type="text"
          name="username"
          placeholder="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          name="password"
          placeholder="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" onClick={() => setMode("login")}>
          Login
        </button>
        <button type="submit" onClick={() => setMode("register")}>
          Register
        </button>
      </form>
    </div>
  );
}

export default ChatAuthen;
