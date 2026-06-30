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

  const isAuthenticated = !!localStorage.getItem("access_token");

  const navItems = [
    { title: "Home", path: "/home", publicOnly: true },
    { title: "Features", path: "/features", publicOnly: true },
    { title: "Workspaces", path: "/workspaces", publicOnly: false },
    { title: "About", path: "/about", publicOnly: true },
  ];

  const visibleNavItems = navItems;

  return (
    <header className="public-header">
      <div className="header-logo" onClick={() => navigate(isAuthenticated ? "/workspaces" : "/home")}>
        INFRAMIND
      </div>

      <nav className="header-nav">
        {visibleNavItems.map((item) => (
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
        {isAuthenticated ? (
          <>
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
          </>
        ) : (
          <button className="cta-btn" onClick={() => navigate("/auth")} style={{ padding: "8px 16px", borderRadius: "6px", border: "none", background: "var(--primary-color, #007bff)", color: "#fff", cursor: "pointer", fontWeight: "bold" }}>
            Login
          </button>
        )}
      </div>
    </header>
  );
};

export default PublicHeader;
