import React from "react";

import { logOutHandle } from "../util/ChatHttp";

function ChatDashboard({ username, onLogout }) {
  function handleLogout() {
    logOutHandle()
      .then(() => {
        onLogout(null);
      })
      .catch((error) => {
        console.error("Error during logout:", error);
        alert(error.message);
      });
    onLogout(null);
  }

  return (
    <div>
      <h1>Hello, {username}</h1>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default ChatDashboard;
