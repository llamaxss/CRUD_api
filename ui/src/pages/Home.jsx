import { Outlet, useNavigate } from "react-router-dom";

import "./Home.css"

function Home() {
  const navigate = useNavigate();

  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    <div>
      <nav>
        <ul>
          <li>
            <button onClick={() => handleNavigation("/")}>Home</button>
          </li>
          <li>
            <button onClick={() => handleNavigation("/blog")}>blog</button>
          </li>
          <li>
            <button onClick={() => handleNavigation("/weather")}>
              weather
            </button>
          </li>
          <li>
            <button onClick={() => handleNavigation("/chat")}>chat</button>
          </li>
        </ul>
      </nav>
      <Outlet />
    </div>
  );
}

export default Home;
