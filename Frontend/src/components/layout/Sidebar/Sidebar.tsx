import {
  Activity,
  ArrowLeftRight,
  Brain,
  ChartColumn,
  ChevronLeft,
  ChevronRight,
  LayoutDashboard,
  LogOut,
  Settings,
  TrendingUp,
} from "lucide-react";
import { useState } from "react";
import { NavLink, useNavigate, useParams } from "react-router-dom";
import { useWorkspace } from "../../../context/WorkspaceContext.tsx";
import "./Sidebar.css";

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const { id } = useParams();

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  const { workspace } = useWorkspace();

  const menuItems = [
    {
      title: "Dashboard",
      icon: <LayoutDashboard />,
      path: `/workspaces/${id}/dashboard`,
    },
    {
      title: "AI Analysis",
      icon: <Brain />,
      path: `/workspaces/${id}/insights`,
    },
    {
      title: "Predictions",
      icon: <TrendingUp />,
      path: `/workspaces/${id}/predictions`,
    },
    {
      title: "Trends",
      icon: <ChartColumn />,
      path: `/workspaces/${id}/trends`,
    },
    { title: "Configuration", icon: <Settings />, path: `/workspaces/${id}/setup` },
  ];

  return (
    <aside className={collapsed ? "sidebar collapsed" : "sidebar"}>
      <div>
        <div className="sidebar-header">
          <div className="logo">{collapsed ? "IM" : "InfraMind"}</div>
          <button
            className="collapse-btn"
            onClick={() => setCollapsed(!collapsed)}
          >
            {collapsed ? <ChevronRight /> : <ChevronLeft />}
          </button>
        </div>

        <div className="workspace-card">
          <div className="workspace-icon">
            <Activity />
          </div>
          {!collapsed && (
            <div className="workspace-details">
              <h3>{workspace.name}</h3>
              <div className="workspace-status">
                <div
                  className={
                    workspace.is_active
                      ? "status-dot active"
                      : "status-dot inactive"
                  }
                />
                {workspace.is_active ? "Healthy" : "Inactive"}
              </div>
            </div>
          )}
        </div>

        <div className="menu-section">
          {menuItems.map((item) => (
            <NavLink
              key={item.title}
              to={item.path}
              className={({ isActive }) =>
                isActive ? "menu-item active" : "menu-item"
              }
            >
              <div className="menu-icon">{item.icon}</div>
              {!collapsed && <span>{item.title}</span>}
            </NavLink>
          ))}
        </div>
      </div>

      <div className="bottom-menu">
        <button className="menu-item" onClick={() => navigate("/workspaces")}>
          <div className="menu-icon">
            <ArrowLeftRight />
          </div>
          {!collapsed && <span>Switch Workspace</span>}
        </button>
        <button className="menu-item" onClick={logout}>
          <div className="menu-icon">
            <LogOut />
          </div>
          {!collapsed && <span>Logout</span>}
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
