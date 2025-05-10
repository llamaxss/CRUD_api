import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./App.css";

import Home from "./pages/Home";
import Blog from "./pages/Blog";
import Weather from "./pages/Weather";
import Chat from "./pages/ChatHome";

const route = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
    children: [
      { path: "blog", element: <Blog /> },
      { path: "weather", element: <Weather /> },
      {
        path: "chat",
        element: <Chat />,
      },
    ],
    errorElement: <div>Oops! Something went wrong.</div>,
  },
]);

function App() {
  return <RouterProvider router={route} />;
}

export default App;
