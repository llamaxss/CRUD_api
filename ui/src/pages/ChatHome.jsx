import React, { useState } from "react";
import { Outlet } from "react-router-dom";

import ChatAuthen from "../components/ChatAuthen";
import ChatDashboard from "../components/ChatDashboard";

function ChatHome() {
  const [user, setUser] = useState();

  return (
    <>
      {user ? (
        <ChatDashboard username={user} onLogout={setUser} />
      ) : (
        <ChatAuthen onSubmit={setUser} />
      )}
    </>
  );
}

export default ChatHome;
