import "./PublicHeader.css";

import { useState } from "react";

import { useLocation, useNavigate } from "react-router-dom";

import { LogOut, User } from "lucide-react";

const PublicHeader = () => {
  const navigate = useNavigate();

  const location = useLocation();

  const [open, setOpen] = useState(false);

  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const logout = () => {
    localStorage.clear();

    navigate("/auth");
  };

  const navItems = [
    {
      title: "Home",

      path: "/home",
    },

    {
      title: "Features",

      path: "/features",
    },

    {
      title: "Workspaces",

      path: "/workspaces",
    },

    {
      title: "About",

      path: "/about",
    },
  ];

  return (
    <header className="public-header">
      <div className="header-logo" onClick={() => navigate("/home")}>
        INFRAMIND
      </div>

      <nav className="header-nav">
        {navItems.map((item) => (
          <button
            key={item.title}
            className={location.pathname === item.path ? "active" : ""}
            onClick={() => navigate(item.path)}
          >
            {item.title}
          </button>
        ))}
      </nav>

      <div className="header-user">
        <button className="user-btn" onClick={() => setOpen(!open)}>
          <div className="avatar">
            {user?.username ? user.username[0].toUpperCase() : "U"}
          </div>

          <span>{user?.username || "User"}</span>
        </button>

        {open && (
          <div className="user-dropdown">
            <button onClick={() => navigate("/profile")}>
              <User size={18} />
              Profile
            </button>

            <button onClick={logout}>
              <LogOut size={18} />
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default PublicHeader;
